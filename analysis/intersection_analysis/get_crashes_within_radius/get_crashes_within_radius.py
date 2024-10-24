import geopandas as gpd
from shapely.geometry import Point
import warnings

# Suppress specific runtime warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


def get_crashes_within_radius(crashes, intersections, intersection_buffer_ft, epsg, projected_crs):
    # Convert buffer from feet to meters
    intersection_buffer_m = intersection_buffer_ft * 0.3048

    # Step 1: Convert the crash dataframe to a GeoDataFrame using 'latitude' and 'longitude'
    crashes['geometry'] = crashes.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)
    crashes_gdf = gpd.GeoDataFrame(crashes, geometry='geometry')

    # Step 2: Ensure both the crashes and intersections are in the same CRS
    if crashes_gdf.crs is None:
        crashes_gdf.set_crs(epsg=epsg, inplace=True)

    if intersections.crs is None:
        intersections.set_crs(epsg=epsg, inplace=True)

    # Step 3: Reproject to a CRS that uses meters for distance calculations
    intersections = intersections.to_crs(epsg=projected_crs)
    crashes_gdf = crashes_gdf.to_crs(epsg=projected_crs)

    # Step 4: Buffer the intersections by the desired radius (in meters)
    intersections['geometry'] = intersections.geometry.buffer(intersection_buffer_m)

    # Step 5: Perform a spatial join to merge crashes with buffered intersections
    # This will link all crashes that fall within the buffered area of each intersection
    crashes_near_intersections = gpd.sjoin(crashes_gdf, intersections, how="inner", predicate='within')

    # Step 6: Return the merged data (all crashes within intersection buffers)
    return crashes_near_intersections
