import json

def focused_column_cleaner(crash_records, focused_columns):

    filtered_crash_records = crash_records[focused_columns]

    return filtered_crash_records