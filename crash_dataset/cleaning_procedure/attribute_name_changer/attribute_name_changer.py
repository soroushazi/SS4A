

def attribute_name_changer(crash_records, attributes_names):
    """
    Renames the columns of a DataFrame using the given mapping.
    
    Parameters:
    crash_records : pandas.DataFrame
        The DataFrame whose columns need to be renamed.
    attributes_mapping : dict
        A dictionary where the keys are the new column names and the values are the current column names in the DataFrame.
    
    Returns:
    pandas.DataFrame
        A DataFrame with renamed columns.
    """

    # the mapping the dictionary
    mapping = {k: v for k, v in attributes_names.items() if k in crash_records.columns}
    
    # Rename the columns in the DataFrame
    crash_records = crash_records.rename(columns=mapping)
    
    return crash_records

