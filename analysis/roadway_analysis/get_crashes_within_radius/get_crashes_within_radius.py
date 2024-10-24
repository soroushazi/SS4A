import geopandas as gpd
from shapely.geometry import Point
import warnings

# Suppress specific runtime warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


def get_crashes_within_radius(crashes, roadways, roadway_buffer_ft, epsg, projected_crs):
    # Convert buffer from feet to meters
    roadway_buffer_m = roadway_buffer_ft * 0.3048

    # Step 1: Convert the crash dataframe to a GeoDataFrame using 'latitude' and 'longitude'
    crashes['geometry'] = crashes.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
    crashes_gdf = gpd.GeoDataFrame(crashes, geometry='geometry')

    # Step 2: Ensure both the crashes and roadways are in the same CRS
    if crashes_gdf.crs is None:
        crashes_gdf.set_crs(epsg=epsg, inplace=True)

    if roadways.crs is None:
        roadways.set_crs(epsg=epsg, inplace=True)

    # Step 3: Reproject to a CRS that uses meters for distance calculations
    roadways = roadways.to_crs(epsg=projected_crs)
    crashes_gdf = crashes_gdf.to_crs(epsg=projected_crs)

    # Step 4: Buffer the roadways by the desired radius (in meters)
    roadways['geometry'] = roadways.geometry.buffer(roadway_buffer_m)

    # Step 5: Perform a spatial join to merge crashes with buffered roadways
    # This will link all crashes that fall within the buffered area of each roadway
    crashes_near_roadways = gpd.sjoin(crashes_gdf, roadways, how="inner", predicate='within')

    # Step 6: Return the merged data (all crashes within roadway buffers)
    return crashes_near_roadways
