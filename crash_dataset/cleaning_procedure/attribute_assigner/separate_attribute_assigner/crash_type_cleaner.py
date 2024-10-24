import json


def crash_type_cleaner(unique_crash_records):

    # Getting the attributes Names
    configs_path = 'crash_dataset/configs/configs.json' 
    with open(configs_path, 'r') as f:
        configs = json.load(f)
    attributes_names = configs.get('attributes_names')
    crash_type_column_name = attributes_names.get('Type of Collision (Derived)')
    main_crash_type_column_name = attributes_names.get('main_crash_type')

    unique_crash_records[main_crash_type_column_name] = unique_crash_records[crash_type_column_name].apply(lambda x: 'FIXED-OBJECT' if 'F-O' in x else x)

    return unique_crash_records

