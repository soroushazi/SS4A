import pandas as pd
import geopandas as gpd

import jenkspy

import warnings

# Suppress the warning about truncated column names in Shapefiles
warnings.filterwarnings("ignore", message="Column names longer than 10 characters will be truncated when saved to ESRI Shapefile.")

# Suppress the warning about missing CRS when saving a dataset
warnings.filterwarnings("ignore", message="'crs' was not provided. The output dataset will not have projection information defined and may not be usable in other systems.")
warnings.filterwarnings("ignore", message="'crs' was not provided.  The output dataset will not have projection information defined and may not be usable in other systems.")


def total_crashes_counter(merged_crashes, number_of_categories):

    # Step 1: Aggregate non-geometry columns
    intersections_crash_counter = merged_crashes.groupby('intersection_id').agg(

        total_crashes=('crash_id', 'count')
    
    ).reset_index()


    # Step 2: Get the geometry (intersection_location) using 'first' for each group
    intersection_geometries = merged_crashes.groupby('intersection_id')['intersection_location'].first().reset_index()

    # Step 3: Merge the aggregated non-geometry data with the geometry data
    intersections_crash_counter = intersections_crash_counter.merge(intersection_geometries, on='intersection_id')

    # Step 4: Convert the result back to a GeoDataFrame
    intersections_crash_counter = gpd.GeoDataFrame(intersections_crash_counter, geometry='intersection_location')

    # Step 5: Sort by total_crashes
    intersections_crash_counter = intersections_crash_counter.sort_values(by='total_crashes', ascending=False).reset_index()

    
    ##### Categorizing the total_crashes into groups #####
    crashes_values = intersections_crash_counter['total_crashes'].values
    crashes_breaks = jenkspy.jenks_breaks(crashes_values, n_classes=number_of_categories)

    def total_crashes_categorizer(crashes_values, crashes_breaks):
        if crashes_values >= crashes_breaks[2]:
            return 'High'
        elif (crashes_values >= crashes_breaks[1]) and (crashes_values < crashes_breaks[2]):
            return 'Medium'
        elif crashes_values < crashes_breaks[1]:
            return 'Low'

    intersections_crash_counter.loc[:, 'group'] = intersections_crash_counter['total_crashes'].apply(lambda x: total_crashes_categorizer(x, crashes_breaks))
    
    return intersections_crash_counter


