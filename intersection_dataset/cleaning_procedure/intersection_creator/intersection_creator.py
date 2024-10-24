import json

import pandas as pd
import geopandas as gpd

import warnings

# Suppress specific runtime warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


def intersection_creator(roadway_network, raw_intersection_save_path):


# Create an empty GeoDataFrame to store intersection points
    intersection_points = gpd.GeoDataFrame(columns=['geometry'], geometry='geometry')

    # Iterate over each pair of geometries in the GeoDataFrame
    for i, road1 in roadway_network.iterrows():
        for j, road2 in roadway_network.loc[i+1:].iterrows():  # Avoid checking the same pair twice
            if road1.geometry.intersects(road2.geometry):
                # Find the intersection point
                intersection = road1.geometry.intersection(road2.geometry)
                
                # If the intersection is a point or multiple points, store it
                if intersection.is_empty:
                    continue
                elif intersection.geom_type == 'Point':
                    # Use pd.concat to add the intersection point
                    intersection_points = pd.concat([intersection_points, gpd.GeoDataFrame({'geometry': [intersection]})], ignore_index=True)
                elif intersection.geom_type == 'MultiPoint':
                    # Iterate through each point in the MultiPoint object
                    for point in intersection.geoms:
                        intersection_points = pd.concat([intersection_points, gpd.GeoDataFrame({'geometry': [point]})], ignore_index=True)

    # Set the coordinate reference system (CRS) to match your roadway data
    intersection_points.crs = roadway_network.crs

    # Save the intersection points as a new shapefile if needed
    intersection_points.to_file(raw_intersection_save_path)




