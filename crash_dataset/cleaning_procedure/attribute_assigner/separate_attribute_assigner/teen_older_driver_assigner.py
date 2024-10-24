import json


def teen_older_driver_assigner(crash_records):
    
    # Getting the attributes Names
    configs_path = 'crash_dataset/configs/configs.json' 
    with open(configs_path, 'r') as f:
        configs = json.load(f)
    attributes_names = configs.get('attributes_names')

    crash_id_column_name = attributes_names.get('Doc ID')
    unit_type_column_name = attributes_names.get('Unit Type')
    age_column_name = attributes_names.get('Age')
    teen_driver_column_name = attributes_names.get('teen_driver')
    older_driver_column_name = attributes_names.get('older_driver')

    young_threshold = configs.get('young_driver_threshold')
    older_threshold = configs.get('older_driver_threshold')

    # Some rare cases do not have age => filling those
    crash_records['age'] = crash_records['age'].fillna(0)
    
    
    older_driver_related_crashe_ids = list(crash_records[(crash_records[unit_type_column_name] == 'D') &
                                                         (crash_records[age_column_name] >= older_threshold)][crash_id_column_name].unique())
    
    crash_records[older_driver_column_name] = crash_records[crash_id_column_name].isin(older_driver_related_crashe_ids).astype(int)


    teen_driver_related_crashe_ids = list(crash_records[(crash_records[unit_type_column_name] == 'D') &
                                                        (crash_records[age_column_name] <= young_threshold) &
                                                        (crash_records[age_column_name] > 0)][crash_id_column_name].unique())
    
    crash_records[teen_driver_column_name] = crash_records[crash_id_column_name].isin(teen_driver_related_crashe_ids).astype(int)

    return crash_records
