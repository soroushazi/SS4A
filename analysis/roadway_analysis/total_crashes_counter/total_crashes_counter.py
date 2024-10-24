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
    roadways_crash_counter = merged_crashes.groupby('roadway_index').agg(

        total_crashes=('crash_id', 'count')
    
    ).reset_index()


    # Step 2: Get the geometry (roadway location) using 'first' for each group
    roadway_geometries = merged_crashes.groupby('roadway_index')['geometry'].first().reset_index()

    # Step 3: Merge the aggregated non-geometry data with the geometry data
    roadways_crash_counter = roadways_crash_counter.merge(roadway_geometries, on='roadway_index')

    # Step 4: Convert the result back to a GeoDataFrame
    roadways_crash_counter = gpd.GeoDataFrame(roadways_crash_counter, geometry='geometry')

    # Step 5: Sort by total_crashes
    roadways_crash_counter = roadways_crash_counter.sort_values(by='total_crashes', ascending=False).reset_index()

    
    ##### Categorizing the total_crashes into groups #####
    crashes_values = roadways_crash_counter['total_crashes'].values
    crashes_breaks = jenkspy.jenks_breaks(crashes_values, n_classes=number_of_categories)

    def total_crashes_categorizer(crashes_values, crashes_breaks):
        if crashes_values >= crashes_breaks[2]:
            return 'High'
        elif (crashes_values > crashes_breaks[1]) and (crashes_values < crashes_breaks[2]):
            return 'Medium'
        elif crashes_values <= crashes_breaks[1]:
            return 'Low'

    roadways_crash_counter.loc[:, 'group'] = roadways_crash_counter['total_crashes'].apply(lambda x: total_crashes_categorizer(x, crashes_breaks))
    
    return roadways_crash_counter


