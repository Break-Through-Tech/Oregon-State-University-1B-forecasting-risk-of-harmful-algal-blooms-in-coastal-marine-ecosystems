
"""
This script shows how you can use the copernicusmarine library to obtain ocean data
that corresponds to an event. The process can be scaled up to match data to many
individual events to identify ocean conditions that correlate with an outcome of
interest.
"""
import copernicusmarine
from datetime import timedelta
from datetime import datetime
import matplotlib.pyplot as plt
from pathlib import Path

# Define a hypothetical event we want to match data to 
EVENT_NAME = "Chilean salmon mortality"
EVENT_DATE = datetime.strptime("2023-02-12", "%Y-%m-%d")
tolerance = timedelta(hours=12)
EVENT_LAT = -43.81
EVENT_LON = -73.66

###  Define data set to access ###
# This is the Copernicus Marine global ocean physics reanalysis
ds = copernicusmarine.open_dataset(
    dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
)

# Select the variable, region, and date of interest. This stays lazy: nothing is
# downloaded until a compute step below forces it.
region = ds["thetao"].sel(
    longitude=slice(EVENT_LON-1.0, EVENT_LON+1.0),
    latitude=slice(EVENT_LAT-1.0, EVENT_LAT+1.0),
    time=EVENT_DATE,  
    depth=slice(0,1.0)
)


# Plot the data for the date of interest 
region.plot(cmap='viridis')
plt.savefig("example_sst.png")


# Calculate statistics over the selected region and time
print("Average temperature",region.mean().compute().item())
print("99th percentile of temperature", region.quantile(0.99).compute().item())



# Use the subset function to download data over the area of interest
output_file = f"{EVENT_NAME}_{EVENT_DATE-tolerance}_{EVENT_DATE+tolerance}_sst.nc"
if Path(f"copernicusmarine/{output_file}").exists():
    print("Data already loaded")
else:
    copernicusmarine.subset(
        dataset_id="cmems_mod_glo_phy_my_0.083deg_P1D-m",
        variables=["thetao"], # temperature
        minimum_longitude=EVENT_LON-0.5, maximum_longitude=EVENT_LON+0.5,
        minimum_latitude=EVENT_LAT-0.5, maximum_latitude=EVENT_LAT+0.5,
        start_datetime=EVENT_DATE-tolerance,
        end_datetime=EVENT_DATE+tolerance,
        minimum_depth=0, maximum_depth=1, # extract surface conditions 
        coordinates_selection_method="nearest",
        output_directory="copernicusmarine",
        output_filename=output_file,
    )

