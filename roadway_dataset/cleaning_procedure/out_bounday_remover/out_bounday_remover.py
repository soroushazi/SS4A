import json

import geopandas as gpd

import warnings

# Suppress specific runtime warnings
warnings.filterwarnings("ignore")


def out_boundary_remover(roadway_network_path, study_boundary_path, epsg, cleaned_roadway_network_path):

    """
    Filters crash records based on their geographical location, ensuring they fall within a given boundary.

    Parameters:
    -----------
    roadway_network : path to geopandas.GeoDataFrame
        Path to a GeoDataFrame representing the roadway network working on.
    
    boundary_shapefile_path : path to geopandas.GeoDataFrame
        Path to a GeoDataFrame representing the boundary within which the roadway network need to be filtered.

    Returns:
    --------
    list
        A list of unique crash IDs that fall within the specified boundary.
    """

    # Reading the roadway network file
    roadway_gdf = gpd.read_file(roadway_network_path)

    # Load the study boundary shapefile file
    study_boundary_gdf = gpd.read_file(study_boundary_path)

    # Setting the CRS (coordinate reference system) to the correct EPSG code
    study_boundary_gdf = study_boundary_gdf.to_crs(epsg)

    # Perform the spatial intersection to keep only the road segments within the study boundary
    filtered_roadway_gdf = gpd.overlay(roadway_gdf, study_boundary_gdf, how='intersection')

    # Save the filtered roadway network as a new shapefile
    filtered_roadway_gdf.to_file(cleaned_roadway_network_path)

    return filtered_roadway_gdf
