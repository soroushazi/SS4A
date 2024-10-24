import pandas as pd
import geopandas as gpd

import jenkspy

import warnings

# Suppress the warning about truncated column names in Shapefiles
warnings.filterwarnings("ignore", message="Column names longer than 10 characters will be truncated when saved to ESRI Shapefile.")

# Suppress the warning about missing CRS when saving a dataset
warnings.filterwarnings("ignore", message="'crs' was not provided. The output dataset will not have projection information defined and may not be usable in other systems.")
warnings.filterwarnings("ignore", message="'crs' was not provided.  The output dataset will not have projection information defined and may not be usable in other systems.")


def crash_rate_calculator(merged_crashes, epdo_rates, severity_levels, number_of_epdo_categories):

    # Only focusing on the severity levels we are looking for
    merged_crashes = merged_crashes[merged_crashes['severity_level'].isin(severity_levels)]

    merged_crashes.loc[:, 'epdo_raw'] = merged_crashes['severity_level'].apply(lambda x: epdo_rates[x])

    # Dummies for severity levels
    severity_level_dummies = pd.get_dummies(merged_crashes['severity_level'],
                                                       prefix='',
                                                       prefix_sep='').astype(int)
    merged_crashes = pd.concat([merged_crashes, severity_level_dummies], axis=1)


    ##### Calculating the EPDO #####
    # Step 1: Aggregate non-geometry columns
    if 'property_damage' in severity_levels:
        intersections_epdo = merged_crashes.groupby('intersection_id').agg(

            fatal_crashes=('fatal', 'sum'),
            incapacitating_injury_crashes=('incapacitating_injury', 'sum'),
            non_incapacitating_injury_crashes=('non_incapacitating_injury', 'sum'),
            possible_injury_crashes=('possible_injury', 'sum'),
            property_damage_crashes=('property_damage', 'sum'),

            epdo=('epdo_raw', 'sum')
        
        ).reset_index()
    else:
        intersections_epdo = merged_crashes.groupby('intersection_id').agg(

            fatal_crashes=('fatal', 'sum'),
            incapacitating_injury_crashes=('incapacitating_injury', 'sum'),
            non_incapacitating_injury_crashes=('non_incapacitating_injury', 'sum'),
            possible_injury_crashes=('possible_injury', 'sum'),

            epdo=('epdo_raw', 'sum')
        
        ).reset_index()


    # Step 2: Get the geometry (intersection_location) using 'first' for each group
    intersection_geometries = merged_crashes.groupby('intersection_id')['intersection_location'].first().reset_index()

    # Step 3: Merge the aggregated non-geometry data with the geometry data
    intersections_epdo = intersections_epdo.merge(intersection_geometries, on='intersection_id')

    # Step 4: Convert the result back to a GeoDataFrame
    intersections_epdo = gpd.GeoDataFrame(intersections_epdo, geometry='intersection_location')

    # Step 5: Sort by EPDO
    intersections_epdo = intersections_epdo.sort_values(by='epdo', ascending=False).reset_index()

    
    ##### Categorizing the EPDO into groups #####
    epdo_values = intersections_epdo['epdo'].values
    epdo_breaks = jenkspy.jenks_breaks(epdo_values, n_classes=number_of_epdo_categories)

    def epdo_categorizer(epdo_value, epdo_breaks):
        if epdo_value >= epdo_breaks[2]:
            return 'High'
        elif (epdo_value >= epdo_breaks[1]) and (epdo_value < epdo_breaks[2]):
            return 'Medium'
        elif epdo_value < epdo_breaks[1]:
            return 'Low'

    intersections_epdo.loc[:, 'epdo_group'] = intersections_epdo['epdo'].apply(lambda x: epdo_categorizer(x, epdo_breaks))
    
    return intersections_epdo



    