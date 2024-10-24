import json


def alcohol_or_drug_assigner(crash_records):


    # Getting the attributes Names
    configs_path = 'crash_dataset/configs/configs.json' 
    with open(configs_path, 'r') as f:
        configs = json.load(f)
    attributes_names = configs.get('attributes_names')


    crash_id_column_name = attributes_names.get('Doc ID')
    alcohol_column_name = attributes_names.get('Alcohol Involved')
    drug_column_name = attributes_names.get('Drugs Involved')
    alcohol_or_drug_column_name = attributes_names.get('alcohol_or_drug')

    # Whether alcohol or drug involved
    alcohol_drug_related_crashe_ids = list(crash_records[(crash_records[alcohol_column_name] == 'Y') |
                                                                (crash_records[drug_column_name] == 'Y')][crash_id_column_name].unique())

    # fitlering only the ids identified
    crash_records[alcohol_or_drug_column_name] = crash_records[crash_id_column_name].isin(alcohol_drug_related_crashe_ids).astype(int)

    return crash_records
