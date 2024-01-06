import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Load shapefile
shapefile_path = 'D:\sop_stuff\India.shp'
gdf = gpd.read_file(shapefile_path)

# Load NetCDF file
netcdf_path = 'D:\sop_stuff\landslide.nc'
ds = xr.open_dataset(netcdf_path)

# Define latitude and longitude ranges
lat_range = slice(14, 16)
lon_range = slice(73, 75)

# Clip the data based on latitude and longitude
ds_clipped = ds.sel(LATITUDE=lat_range, LONGITUDE=lon_range)

# Filter data for June and July
rainfall_june_july = ds_clipped['RAINFALL'].sel(TIME=slice('2022-06', '2022-07')).mean(dim='TIME')

# Plotting
fig, ax = plt.subplots(figsize=(10, 12))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

# Plot the shapefile
gdf.boundary.plot(ax=ax, linewidth=1)

# Plot the clipped rainfall data
pcm = ax.pcolormesh(ds_clipped['LONGITUDE'], ds_clipped['LATITUDE'], rainfall_june_july, shading='auto', cmap='Blues')

# Add colorbar
cbar = fig.colorbar(pcm, cax=cax)
cbar.set_label('Rainfall (cm)')

# Set plot title and labels
plt.title('Clipped Rainfall Distribution (June-July 2022)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Save the plot to a file (you can choose either PNG or JPEG)
plt.savefig('clipped_rainfall_map.png', bbox_inches='tight')
# or
# plt.savefig('clipped_rainfall_map.jpg', bbox_inches='tight')

# Display the plot
plt.show()
