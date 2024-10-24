

def severity_level_cleaner(crash_records, attributes_names, acceptable_severity_levels):

    """
    Filters crash records based on acceptable severity levels and returns unique crash IDs.

    Parameters:
    - crash_records: DataFrame containing crash records
    - crash_id_column_name: Name of the column representing crash IDs
    - severity_level_column_name: Name of the column representing severity levels
    - acceptable_severity_levels: List of acceptable severity levels

    Returns:
    - List of unique crash IDs with acceptable severity levels
    """
    
    crash_id_column_name = attributes_names.get('Doc ID')
    severity_level_column_name = attributes_names.get('Severity')

    unique_crash_records = crash_records.drop_duplicates(subset=crash_id_column_name, keep='first')

    filtered_crash_records = unique_crash_records[unique_crash_records[severity_level_column_name].isin(acceptable_severity_levels)]

    return filtered_crash_records
