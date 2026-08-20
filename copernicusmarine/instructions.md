# Working with Copernicus Marine Service Data

The Copernicus Marine Service (CMEMS) provides high quality data products that use physics based models to reconstruct past ocean conditions and forecast future events. We will be accessing these data using the Copernicus Marine Toolbox. Using these data requires a free account that you can register for here: https://marine.copernicus.eu/. Once you have an account you can load data using the `copernicusmarine` python library, which provides an API for searching and accessing CMEMS data products.

## Building a conda environment for accessing CMEMS data
The best practice is to use [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) to manage dependencies when working with geospatial data. You can use the environment.yml file to build a conda environment called `cmems` that has all of the dependencies needed to work with the Copernicus Marine Toolbox.

The following block of terminal commands will build the conda environment and prompt you to enter your login credentials for the CMEMS data.

```
conda env create -f environment.yml   # or: mamba env create -f environment.yml
conda activate cmems
copernicusmarine login
```

## Working with the Copernicus Marine Toolbox python API

Documentation for the Copernicus Marine Toolbox can be found [here](https://toolbox-docs.marine.copernicus.eu/en/stable/). It provides both command line and python interfaces. The most useful functions for our analysis will likely be the `open_dataset` and `subset` functions.

`open_dataset` provides access to CMEMS data sets as xarray objects. It only loads the subsets of the data into memory that are required for calculations. It can be used to calculate statistics, generate plots, and perform other computations.

`subset` allows you to download subsets of data that fall within a defined time span and geographic range. This is ideal if you need to store data as geospatial grids.

The `example.py` file shows how these two methods can be used to obtain data from CMEMS.
