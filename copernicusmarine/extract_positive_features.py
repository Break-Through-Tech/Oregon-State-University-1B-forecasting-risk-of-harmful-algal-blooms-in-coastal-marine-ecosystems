from pathlib import Path
from datetime import timedelta
import tempfile

import pandas as pd
import xarray as xr
import copernicusmarine
from dotenv import load_dotenv


load_dotenv()

ROOT = Path(__file__).resolve().parents[1]

INPUT = ROOT / "data" / "raw" / "harmful_algae_events.csv"
OUTPUT = ROOT / "data" / "processed" / "haedat_copernicus_features.csv"

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
TIME_WINDOW = timedelta(hours=12)


def filter_events(df):
    df = df.copy()

    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

    # Design choice:
    # Event Date first, Start Date as fallback
    df["date"] = pd.to_datetime(
        df["Event Date"].fillna(df["Start Date"]),
        errors="coerce",
    )

    return df[
        df["Latitude"].between(-90, 90)
        & df["Longitude"].between(-180, 180)
        & df["date"].notna()
        & (df["Freshwater"] == "No")
        & (df["Status"] == "Approved")
        & (df["date"] >= "1993-01-01")
    ].copy()


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

    df = pd.read_csv(INPUT, low_memory=False)
    df = filter_events(df)

    print(f"Positive events: {len(df):,}")

    rows = []

    for i, (_, event) in enumerate(df.iterrows(), 1):

        print(f"[{i}/{len(df)}] Event {event['Event ID']}")

        try:
            features = extract_features(
                float(event["Latitude"]),
                float(event["Longitude"]),
                event["date"],
            )

            rows.append({
                "Event ID": event["Event ID"],
                "Country": event["Country"],
                "Latitude": event["Latitude"],
                "Longitude": event["Longitude"],
                "date": event["date"],
                **features,
                "label": 1,
            })

        except Exception as e:
            print(f"ERROR: {e}")

    pd.DataFrame(rows).to_csv(OUTPUT, index=False)

    print(f"\nSaved {len(rows):,} rows")
    print(OUTPUT)


if __name__ == "__main__":
    main()