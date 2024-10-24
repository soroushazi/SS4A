import json


def sleepy_ill_dizzy_driver_assigner(crash_records):

    # Getting the attributes Names
    configs_path = 'crash_dataset/configs/configs.json' 
    with open(configs_path, 'r') as f:
        configs = json.load(f)
    attributes_names = configs.get('attributes_names')
    person_condition_column_name = attributes_names.get('Person Condition')
    sleepy_ill_dizzy_driver_column_name = attributes_names.get('sleepy_ill_dizzy_driver')

    sleepy_ill_dizzy_driver_conditions = configs.get('sleepy_ill_dizzy_driver_conditions')

    crash_records[sleepy_ill_dizzy_driver_column_name] = crash_records[person_condition_column_name].apply(lambda x: 1 if x in sleepy_ill_dizzy_driver_conditions else 0)

    return crash_records
