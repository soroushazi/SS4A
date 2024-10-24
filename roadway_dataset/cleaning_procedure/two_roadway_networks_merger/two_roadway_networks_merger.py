import pandas as pd
import geopandas as gpd

import json


def two_roadway_networks_merger(first_network_name, first_roadway_shapefile, second_network_name, second_roadway_shapefile):

    # Getting the files_paths from config
    configs_path = 'roadway_dataset/configs/configs.json'
    with open(configs_path, 'r') as f:
        configs = json.load(f)

    merged_roadway_network_path = configs.get('files_paths').get('merged_roadway_network_path')

    # Creating ID column for each of the networks
    first_roadway_shapefile['segment_id'] = range(1, len(first_roadway_shapefile) + 1)
    second_roadway_shapefile['segment_id'] = range(1, len(second_roadway_shapefile) + 1)

    # a column for their network_name
    first_roadway_shapefile['network_name'] = first_network_name
    second_roadway_shapefile['network_name'] = second_network_name

    # Concatenate the two GeoDataFrames
    combined_gdf = gpd.GeoDataFrame(pd.concat([first_roadway_shapefile, second_roadway_shapefile], ignore_index=True))

    # Save the combined GeoDataFrame as a new shapefile
    combined_gdf.to_file(merged_roadway_network_path)

    # continue processing the combined dataset
    return combined_gdf
