import json


def region_assigner(unique_crash_records, attributes_names, regions):
    """
    Takes a DataFrame and assigns a region based on the 'county' column.
    Adds a new 'region' column that will be 'northern' or 'southern', depending on the county.
    
    Parameters:
    unique_crash_records : pandas.DataFrame
        The DataFrame containing the 'county' column.
    
    Returns:
    pandas.DataFrame
        The DataFrame with an added 'region' column.
    """

    region_column_name = attributes_names.get('region')
    county_column_name = attributes_names.get('County #')
        
    # Create a function to determine the region
    def get_region(county):
        for region, counties in regions.items():
            if county in counties:
                return region
        return None
    
    # Apply the function to the 'county' column
    unique_crash_records[region_column_name] = unique_crash_records[county_column_name].apply(get_region)
    
    return unique_crash_records


