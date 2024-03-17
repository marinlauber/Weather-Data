import netCDF4 as nc
from os import listdir
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from datetime import date

# for file in listdir("."):
file = "data/MERRA2_200.instM_2d_lfo_Nx.199408.nc4"
# file = "data/MERRA2_400.instU_2d_asm_Nx.202305.nc4"
# file = "data/MERRA2_100.instU_2d_asm_Nx.198001.nc4"
print(file)
ds = nc.Dataset(file)
print(ds)
# for var in ds.variables.values():
#     print(var)

wind = "U10M"
wind = "SPEEDLML"

# get data
cur_time = date.fromisoformat(ds.RangeBeginningDate)
lat = ds.variables['lat'][:]
lon = ds.variables['lon'][:]
time = ds.variables['time'][:]
print(time)
v = ds.variables[wind][:]

# plot
fig = plt.figure()
fig.subplots_adjust(left=0., right=1., bottom=0., top=0.9)

# add map with coastlines
m = Basemap(projection='moll', llcrnrlat=-90, urcrnrlat=90,\
            llcrnrlon=0, urcrnrlon=360, resolution='c', lon_0=0)
m.drawcoastlines()
# m.drawmapboundary()

# Transforms lat/lon into plotting coordinates for projection
lon2d, lat2d = np.meshgrid(lon, lat)
x, y = m(lon2d, lat2d)

# Plot of air temperature with 11 contour intervals
cs = m.contourf(x, y, np.mean(v,axis=0), 11, cmap=plt.cm.Spectral_r)

cbar = plt.colorbar(cs, orientation='horizontal', shrink=0.5)
cbar.set_label("%s (%s)" % (ds.variables[wind].long_name,\
                            ds.variables[wind].units))
plt.title("%s in %s %s" % (ds.variables[wind].long_name, cur_time.strftime("%B"), cur_time.strftime("%Y")))

plt.show()