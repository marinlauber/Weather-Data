import xarray as xr
import numpy as np
from datetime import date
import scipy
import time
import platform

# read all moth between 1980 and 2020
collection_shortname = 'M2IUNXASM'
collection_longname  = 'instU_2d_asm_Nx'
MERRA2_version = '5.12.4'

# Loop over years and months
for year in range(1980, 2024):
    for month in range(1,13):

        # Note that collection_number changes
        collection_number = 'MERRA2_400'
        if ((year == 2020) & (month == 9)):
            collection_number = 'MERRA2_401'
        if ((year == 2021) & (month in [6,7,8,9])):
            collection_number = 'MERRA2_401'
        if (year < 2011):
            collection_number = 'MERRA2_300'
        if (year < 2001):
            collection_number = 'MERRA2_200'
        if (year < 1992):
            collection_number = 'MERRA2_100'
        if ((year == 2024) and (month > 2)):
            break

        # OPeNDAP URL 
        url = 'https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2_DIURNAL/{}.{}/{}'.format(
               collection_shortname, MERRA2_version, year)
        files_month = ['{}/{}.{}.{}{:0>2d}.nc4'.format(url,collection_number, collection_longname, year, month)]

        # Print
        print("files", files_month)
        print("Opening...(It may take ~ 5 seconds to open one month data)")
        print(" ")

        # Read dataset URLs
        ds = xr.open_mfdataset(files_month)

        # get data we can to keep
        ds = ds.drop_vars(list(ds.drop_vars(["U10M","V10M","lat","lon","time"]).variables.keys()))
        ds = ds.mean(dim="time")
        
        # save
        ds.to_netcdf("data/{}.{}.{}{:0>2d}.nc4".format(collection_number,collection_longname,year,month))
print("Done")