import pandas as pd
import geopandas as gpd

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
        roadways_epdo = merged_crashes.groupby('roadway_index').agg(

            mileage=('length_mi', 'first'),
            aadt=('aadt', 'first'),

            fatal_crashes=('fatal', 'sum'),
            incapacitating_injury_crashes=('incapacitating_injury', 'sum'),
            non_incapacitating_injury_crashes=('non_incapacitating_injury', 'sum'),
            possible_injury_crashes=('possible_injury', 'sum'),
            property_damage_crashes=('property_damage', 'sum'),

            epdo_raw=('epdo_raw', 'sum')
        
        ).reset_index()

        sum_epdo = 12_637_800

    else:
        roadways_epdo = merged_crashes.groupby('roadway_index').agg(

            mileage=('length_mi', 'first'),
            aadt=('aadt', 'first'),

            fatal_crashes=('fatal', 'sum'),
            incapacitating_injury_crashes=('incapacitating_injury', 'sum'),
            non_incapacitating_injury_crashes=('non_incapacitating_injury', 'sum'),
            possible_injury_crashes=('possible_injury', 'sum'),

            epdo_raw=('epdo_raw', 'sum')
        
        ).reset_index()

        sum_epdo = 12_633_600

    roadways_epdo['epdo'] = (
    (roadways_epdo['epdo_raw'] * 100_000_000) /
    (365 * 5 * roadways_epdo['aadt'] * roadways_epdo['mileage'] * sum_epdo)
    )


    # Step 2: Get the geometry (roadway_location) using 'first' for each group
    roadway_geometries = merged_crashes.groupby('roadway_index')['geometry'].first().reset_index()

    # Step 3: Merge the aggregated non-geometry data with the geometry data
    roadways_epdo = roadways_epdo.merge(roadway_geometries, on='roadway_index')

    # Step 4: Convert the result back to a GeoDataFrame
    roadways_epdo = gpd.GeoDataFrame(roadways_epdo, geometry='geometry')

    # Step 5: Sort by EPDO
    roadways_epdo = roadways_epdo.sort_values(by='epdo', ascending=False).reset_index()

    
    ##### Categorizing the EPDO into groups #####
    def epdo_categorizer(epdo_value):
        if epdo_value >= 60:
            return 'High'
        elif (epdo_value >= 25) and (epdo_value < 60):
            return 'Medium'
        elif epdo_value < 25:
            return 'Low'

    roadways_epdo.loc[:, 'epdo_group'] = roadways_epdo['epdo'].apply(lambda x: epdo_categorizer(x))
    
    return roadways_epdo



    