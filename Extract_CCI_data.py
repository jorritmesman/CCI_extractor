# Aim: To extract remote sensing data from the CCI database according to
# user defined period, extent of the region and variables of interest.
# Reference: Crétaux et al. (2020): ESA Lakes Climate Change Initiative
# (Lakes_cci): Lake products, Version 1.0. Centre for Environmental Data
# Analysis, 08 June 2020. doi:10.5285/3c324bb4ee394d0d876fe2e1db217378.
#
# Created on 06/04/2022 by Hugo Cruz 
# Contacts: huggcruzz@gmail.com, s.piccolroaz@unitn.it
#########################################################################

import numpy as np
import pandas as pd
import xarray as xr
from packaging.version import Version

ver = '2.0'

start = "2020-01-01"
end = "2020-01-01"
date_range = pd.date_range(start = start , end = end, freq="D")

lat = np.array([45.43, 45.90])
lon = np.array([10.50, 10.89]) # Lake Garda

res = 1 / 120

lat_range = np.floor((90 + lat)/res).astype("int")
lat_range_str = str(lat_range).replace(" ", ":1:")

lon_range = np.floor((180 + lon)/res).astype("int")
lon_range_str = str(lon_range).replace(" ", ":1:")

year = list(map(str, date_range.year))
months = ['{:02d}'.format(month) for month in date_range.month]
days = ['{:02d}'.format(day) for day in date_range.day]

first= True
for date in range(0,len(date_range)):
    
    if Version(ver) < Version("2.1"):
        path = ('https://data.cci.ceda.ac.uk/thredds/dodsC/esacci/lakes/data/lake_products/L3S/v'+ ver+ '/'
          +year[date]+ '/'+ months[date]+ '/ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-'
          +year[date]+  months[date]+ days[date]+ '-fv'+ ver+ '.nc?'
          +'lat'+ lat_range_str+ ',lon'+ lon_range_str+ ',time[0:1:0],lake_surface_water_temperature[0:1:0]'
          +lat_range_str + lon_range_str + ','
          +'lswt_quality_level[0:1:0]'+ lat_range_str+ lon_range_str)
    else:
        path = ('https://data.cci.ceda.ac.uk/thredds/dodsC/esacci/lakes/data/lake_products/L3S/v'+ ver+ '/merged_product/'
          +year[date]+ '/'+ months[date]+ '/ESACCI-LAKES-L3S-LK_PRODUCTS-MERGED-'
          +year[date]+  months[date]+ days[date]+ '-fv'+ ver+ '.0.nc?'
          +'lat'+ lat_range_str+ ',lon'+ lon_range_str+ ',time[0:1:0],lake_surface_water_temperature[0:1:0]'
          +lat_range_str + lon_range_str + ','
          +'lswt_quality_level[0:1:0]'+ lat_range_str+ lon_range_str)
    
    
    dataset = xr.open_dataset(path)
    if first:
        combined_dataset = dataset
        first = False
    else: 
        combined_dataset = xr.combine_by_coords([combined_dataset, dataset], combine_attrs='override')

outfile = "CCI_v"+ver+"_"+year[0]+"-"+year[-1]+".nc"
combined_dataset.to_netcdf(outfile)
