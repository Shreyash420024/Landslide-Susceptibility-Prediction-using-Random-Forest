import xarray as xr
import geopandas as gpd
from rasterio.mask import mask
from rasterio.crs import CRS
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely.geometry import MultiPolygon
import numpy as np
import rasterio

# Load shapefile
shapefile_path = 'D:\sop_stuff\India.shp'
gdf = gpd.read_file(shapefile_path)

# Load NetCDF file
# netcdf_path = 'D:\sop_stuff\landslide.nc'
# ds = xr.open_dataset(netcdf_path)

# # Extract necessary variables
# longitude = ds['LONGITUDE'].values
# latitude = ds['LATITUDE'].values

# # Filter data for June and July
# rainfall_june_july = ds['RAINFALL'].sel(TIME=slice('2022-01', '2022-12')).values

# # Create a meshgrid for plotting
# lon, lat = np.meshgrid(longitude, latitude)

# # Plotting Rainfall
# fig, ax = plt.subplots(figsize=(10, 12))
# divider = make_axes_locatable(ax)
# cax = divider.append_axes("right", size="5%", pad=0.1)

# # Plot the shapefile
# gdf.boundary.plot(ax=ax, linewidth=1)

# # Plot the rainfall data for June and July
# pcm = ax.pcolormesh(lon, lat, rainfall_june_july[0, :, :], shading='auto', cmap='Blues')

# # Add colorbar
# cbar = fig.colorbar(pcm, cax=cax)
# cbar.set_label('Rainfall (cm)')

# # Set plot title and labels
# plt.title('Rainfall Distribution and Elevation in India (June-July 2022)')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')

# # Save the plot to a file (you can choose either PNG or JPEG)
# plt.savefig('combined_plot.png', bbox_inches='tight')
# # or
# # plt.savefig('combined_plot.jpg', bbox_inches='tight')

# # Display the plot
# plt.show()

# Function to mask raster data based on a shapefile
def mask_raster_by_shape(raster, shapefile):
    with rasterio.open(raster) as src:
        shape_mask = gpd.read_file(shapefile)
        # Assign CRS to the shapefile if it doesn't have one
        if shape_mask.crs is None:
            shape_mask.crs = CRS.from_epsg(4326)
        shape_mask = shape_mask.to_crs(src.crs)

        # Create a GeoDataFrame with MultiPolygon
        gdf = gpd.GeoDataFrame(geometry=[shape_mask.geometry.unary_union])

        out_image, out_transform = mask(src, gdf.geometry, crop=True)
        out_meta = src.meta.copy()
    return out_image, out_transform, out_meta

# Paths to elevation data and shapefile
elevation_tif_path1 = 'D:\sop_stuff\eastgoa.tif'
elevation_tif_path2 = 'D:\sop_stuff\westgoa.tif'

# Mask elevation data for the specified region
elevation_data1, transform1, meta1 = mask_raster_by_shape(elevation_tif_path1, shapefile_path)
elevation_data2, transform2, meta2 = mask_raster_by_shape(elevation_tif_path2, shapefile_path)

# Plotting Elevation
fig, ax = plt.subplots(figsize=(10, 12))
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

# Plot the elevation data 1
pcm1 = ax.imshow(elevation_data1[0, :, :], cmap='terrain', extent=[transform1[2], transform1[2] + transform1[0] * elevation_data1.shape[2],
                                                                   transform1[5] + transform1[4] * elevation_data1.shape[1], transform1[5]])

# Plot the elevation data 2
pcm2 = ax.imshow(elevation_data2[0, :, :], cmap='terrain', extent=[transform2[2], transform2[2] + transform2[0] * elevation_data2.shape[2],
                                                                   transform2[5] + transform2[4] * elevation_data2.shape[1], transform2[5]])

# Add colorbar
cbar = fig.colorbar(pcm2, cax=cax)
cbar.set_label('Elevation (meters)')

# Set plot title and labels
plt.title('Elevation Map for the Specified Region')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Save the plot to a file (you can choose either PNG or JPEG)
plt.savefig('elevation_map_combined.png', bbox_inches='tight')
# or
# plt.savefig('elevation_map_combined.jpg', bbox_inches='tight')

# Display the plot
plt.show()
