import numpy as np
import pandas as pd
import geopandas as gpd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import xarray as xr

netcdf_path = 'D:\sop_stuff\landslide.nc'
ds = xr.open_dataset(netcdf_path)

latitude = ds['LATITUDE'].values
longitude = ds['LONGITUDE'].values
rainfall = ds['RAINFALL'].values
altitude = ds['ALTITUDE'].values
slope = ds['SLOPE'].values

latitude_1d = latitude.flatten()
longitude_1d = longitude.flatten()
rainfall_1d = rainfall.flatten()
altitude_1d = altitude.flatten()
slope_1d = slope.flatten()

df = pd.DataFrame({
    'latitude': latitude_1d,
    'longitude': longitude_1d,
    'rainfall': rainfall_1d,
    'altitude': altitude_1d,
    'slope': slope_1d,
})

df['landslide_prone'] = ((df['rainfall'] > df['rainfall'].mean() + 2 * df['rainfall'].std()) &
                         (df['slope'] > df['slope'].mean()) &
                         (df['altitude'] > df['altitude'].mean() + 2 * df['altitude'].std())).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    df[['latitude', 'longitude', 'rainfall', 'altitude', 'slope']],
    df['landslide_prone'],
    test_size=0.2,
    random_state=42
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

df_test = df.iloc[y_test.index].copy()
df_test['probability_landslide'] = model.predict_proba(X_test_scaled)[:, 1]

df.update(df_test)

threshold = 0.5  # You can adjust the threshold based on your preference
df['highly_prone'] = df['probability_landslide'] > threshold

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))

ax = gdf.plot(column='highly_prone', cmap='coolwarm', markersize=5, legend=True)
ax.set_title('Areas Highly Prone to Landslides')
