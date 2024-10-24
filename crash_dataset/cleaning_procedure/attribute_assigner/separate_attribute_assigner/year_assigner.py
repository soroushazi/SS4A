import pandas as pd

def year_assigner(crash_records):
    """
    Adds a 'year' column to the DataFrame by extracting the year from the 'date' column.

    Parameters:
    unique_crash_records : pandas.DataFrame
        A DataFrame that contains a 'date' column in a string format or datetime format.

    Returns:
    pandas.DataFrame
        The original DataFrame with an additional 'year' column.
    """
    # Convert the 'date' column to datetime format if it's not already in that format
    crash_records['date'] = pd.to_datetime(crash_records['date'])
    
    # Create a new column 'year' by extracting the year from the 'date' column
    crash_records['year'] = crash_records['date'].apply(lambda x: x.year)

    # Return the updated DataFrame with the 'year' column
    return crash_records
