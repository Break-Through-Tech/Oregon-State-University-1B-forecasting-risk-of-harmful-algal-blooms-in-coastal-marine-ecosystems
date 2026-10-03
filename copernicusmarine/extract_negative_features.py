from pathlib import Path
from datetime import timedelta
import tempfile
import calendar
import random

import pandas as pd
import xarray as xr
import copernicusmarine
from dotenv import load_dotenv


load_dotenv()

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "processed" / "haedat_extractable_events.csv"
OUTPUT = ROOT / "data" / "processed" / "synthetic_negative_features.csv"

DATASET = "cmems_mod_glo_phy_my_0.083deg_P1D-m"

VARIABLES = [
    "thetao",
    "so",
    "bottomT",
    "mlotst",
    "zos",
    "uo",
    "vo",
]

BUFFER = 0.5
SITE_SIZE = 0.5
TIME_WINDOW = timedelta(hours=12)

MIN_DAYS_FROM_BLOOM = 30
MAX_ATTEMPTS = 100
SEED = 42


def load_events():
    df = pd.read_csv(INPUT, low_memory=False)

    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    df = df.dropna(
        subset=["Latitude", "Longitude", "date"]
    ).copy()

    # Group nearby observations into geographic areas
    df["lat_bin"] = (
        df["Latitude"] / SITE_SIZE
    ).round() * SITE_SIZE

    df["lon_bin"] = (
        df["Longitude"] / SITE_SIZE
    ).round() * SITE_SIZE

    return df


def create_negative_date(event, positives, used, rng):
    nearby = positives[
        (positives["lat_bin"] == event["lat_bin"])
        & (positives["lon_bin"] == event["lon_bin"])
    ]

    # Only sample months where HABs have been observed
    active_months = nearby["date"].dt.month.tolist()

    # Prefer years where this site has observations
    years = nearby["date"].dt.year.unique().tolist()

    if len(years) < 2:
        years = (
            positives[
                positives["Country"] == event["Country"]
            ]["date"]
            .dt.year
            .unique()
            .tolist()
        )

    years = [y for y in years if y >= 1993]

    if not years:
        return None

    for _ in range(MAX_ATTEMPTS):

        year = rng.choice(years)
        month = rng.choice(active_months)

        day = rng.randint(
            1,
            calendar.monthrange(year, month)[1],
        )

        date = pd.Timestamp(
            year=year,
            month=month,
            day=day,
        )

        key = (
            round(float(event["Latitude"]), 6),
            round(float(event["Longitude"]), 6),
            date.date(),
        )

        if key in used:
            continue

        # Stay away from known blooms at this site
        distance = (
            nearby["date"] - date
        ).abs().dt.days

        if (distance <= MIN_DAYS_FROM_BLOOM).any():
            continue

        used.add(key)
        return date

    return None


def extract_features(lat, lon, date):
    with tempfile.TemporaryDirectory() as temp_dir:

        filename = "event.nc"

        copernicusmarine.subset(
            dataset_id=DATASET,
            variables=VARIABLES,
            minimum_longitude=max(-180, lon - BUFFER),
            maximum_longitude=min(180, lon + BUFFER),
            minimum_latitude=max(-90, lat - BUFFER),
            maximum_latitude=min(90, lat + BUFFER),
            start_datetime=date - TIME_WINDOW,
            end_datetime=date + TIME_WINDOW,
            minimum_depth=0,
            maximum_depth=1,
            coordinates_selection_method="nearest",
            output_directory=temp_dir,
            output_filename=filename,
        )

        with xr.open_dataset(Path(temp_dir) / filename) as ds:
            ds = ds.sel(time=date, method="nearest")

            features = {}

            for var in VARIABLES:
                x = ds[var].squeeze()

                features[f"{var}_mean"] = float(
                    x.mean(skipna=True).item()
                )

                features[f"{var}_p95"] = float(
                    x.quantile(0.95, skipna=True).item()
                )

                features[f"{var}_var"] = float(
                    x.var(skipna=True).item()
                )

            return features


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    positives = load_events()

    rng = random.Random(SEED)
    used_dates = set()

    # Shuffle anchors
    positives = positives.sample(
        frac=1,
        random_state=SEED,
    ).reset_index(drop=True)

    print(f"Target negatives: {len(positives):,}")

    rows = []

    for i, (_, event) in enumerate(positives.iterrows(), 1):

        date = create_negative_date(
            event,
            positives,
            used_dates,
            rng,
        )

        if date is None:
            continue

        print(
            f"[{i}/{len(positives)}] "
            f"{event['Country']} | {date.date()}"
        )

        try:
            features = extract_features(
                float(event["Latitude"]),
                float(event["Longitude"]),
                date,
            )

            rows.append({
                "Event ID": f"NEG_{len(rows) + 1}",
                "Country": event["Country"],
                "Latitude": event["Latitude"],
                "Longitude": event["Longitude"],
                "date": date,
                **features,
                "label": 0,
            })

        except Exception as e:
            print(f"ERROR: {e}")

    pd.DataFrame(rows).to_csv(
        OUTPUT,
        index=False,
    )

    print(f"\nSaved {len(rows):,} negatives")
    print(OUTPUT)


if __name__ == "__main__":
    main()