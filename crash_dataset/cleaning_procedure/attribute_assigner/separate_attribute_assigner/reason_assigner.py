import json
import pandas as pd

def reason_assigner(crash_records):

    # Getting the attributes Names
    configs_path = 'crash_dataset/configs/configs.json' 
    with open(configs_path, 'r') as f:
        configs = json.load(f)
    attributes_names = configs.get('attributes_names')

    unsafe_unlaw_category_column_name = attributes_names.get('unsafe_unlaw_category')

    reasons_dummies = pd.get_dummies(crash_records[unsafe_unlaw_category_column_name],
                                      prefix='', 
                                      prefix_sep='').astype(int)

    crash_records = pd.concat([crash_records, reasons_dummies], axis=1)

    return crash_records

