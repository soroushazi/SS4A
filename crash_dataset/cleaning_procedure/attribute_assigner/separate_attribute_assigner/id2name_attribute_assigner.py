import json

def attributes_id2name_assigner(crash_records):

    # Getting the attributes Names
    configs_path = 'crash_dataset/configs/configs.json' 
    with open(configs_path, 'r') as f:
        configs = json.load(f)
    attributes_id2name_dict = configs.get('attributes_id2name')

    for category, attribute_dict in attributes_id2name_dict.items():

        # because we are reading json file and json keys cannot be int => need to change the category to int (because some are float) then to str and then map
        crash_records[category] = crash_records[category].fillna('99') # for person_condition specifically
        crash_records[category] = crash_records[category].apply(lambda x: "0" if x == '?' else x) # for intersection_rel specifically
        crash_records[category] = crash_records[category].astype(int).astype(str) 
        crash_records[category] = crash_records[category].map(attribute_dict)

    return crash_records

