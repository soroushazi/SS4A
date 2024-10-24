#################################################################################
## This file removes the crash records that are outside of the study boundary. ##
#################################################################################

import json

import geopandas as gpd
from shapely.geometry import Point


def out_boundary_remover(crash_records, boundary_shapefile_path, attributes_names, epsg):

    """
    Filters crash records based on their geographical location, ensuring they fall within a given boundary.

    Parameters:
    -----------
    crash_records : pandas.DataFrame
        A DataFrame containing crash records, including latitude and longitude information.
    
    boundary_shapefile_path : path to geopandas.GeoDataFrame
        Path to a GeoDataFrame representing the boundary within which the crash records need to be filtered.

    Returns:
    --------
    list
        A list of unique crash IDs that fall within the specified boundary.
    """
    
    latitude_column_name = attributes_names.get('Latitude (Derived)')
    longitude_column_name = attributes_names.get('Longitude (Derived)')

    # Convert crash records (latitude/longitude) into a GeoDataFrame with Point geometry
    geometry = [Point(xy) for xy in zip(crash_records[longitude_column_name], crash_records[latitude_column_name])]
    crash_gdf = gpd.GeoDataFrame(crash_records, geometry=geometry)

    # Set the coordinate reference system (CRS) for the crash GeoDataFrame
    crash_gdf.set_crs(epsg=epsg, inplace=True)

    # Reading the boundary_shapefile from the path
    boundary_shapefile = gpd.read_file(boundary_shapefile_path)

    # Ensure the boundary shapefile is in the same CRS for accurate spatial operations
    boundary_shapefile = boundary_shapefile.to_crs(epsg=epsg)

    # Perform spatial join to filter crashes that fall within the boundary shapefile
    crashes_within_shape = gpd.sjoin(crash_gdf, boundary_shapefile, predicate='within')

    # To remove the added columns by performing the spatial join
    number_of_columns_before_sjoin = len(crash_records.columns)
    crashes_within_shape = crashes_within_shape.iloc[:, :number_of_columns_before_sjoin]

    return crashes_within_shape
