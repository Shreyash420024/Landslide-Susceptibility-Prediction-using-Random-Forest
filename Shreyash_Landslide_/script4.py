import geopandas as gpd
import matplotlib.pyplot as plt

# Path to the shapefile
shapefile_path = 'D:\sop_stuff\DSMW.shp'

# Read the shapefile using geopandas
gdf = gpd.read_file(shapefile_path)

# Plot the shapefile
gdf.plot()
plt.title('Your Shapefile')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()
# import arcpy

# # Paths to your shapefile and layer file
# shapefile_path = r'D:\sop_stuff\DSMW.shp'
# layer_file_path = r'D:\sop_stuff\DSMW.lyr'
# output_shapefile_path = r'D:\sop_stuff\DSMW_with_symbology.shp'

# # Apply symbology from layer file to shapefile
# arcpy.MakeFeatureLayer_management(shapefile_path, "temporary_layer")
# arcpy.ApplySymbologyFromLayer_management("temporary_layer", layer_file_path)
# arcpy.FeatureClassToFeatureClass_conversion("temporary_layer", output_shapefile_path)

# # Now you can use geopandas to read and plot the symbology-applied shapefile
# import geopandas as gpd
# import matplotlib.pyplot as plt

# gdf = gpd.read_file(output_shapefile_path)

# # Plot the shapefile with different colors for different categories
# gdf.plot(legend=True, legend_kwds={'loc': 'upper left'})
# plt.title('Digital Soil Map of the World')
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.show()





