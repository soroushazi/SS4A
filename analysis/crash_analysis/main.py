import json

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pandas as pd

import logging
logging.basicConfig(level=logging.INFO)

from top_reasons_finder.top_reasons_finder import top_reasons_finder
from reason_stat_creator.reason_stat_creator import reason_stat_creator
from reason_stat_creator.only_reason_stat_creator import only_reason_stat_creator
from all_reasons_finder.all_reasons_finder import all_reasons_finder
from error_thrower.error_thrower import error_thrower


################################
## 1. Reading the Config File ##
################################

try:
    configs_path = 'analysis/crash_analysis/configs/configs.json'
    with open(configs_path, 'r') as f:
        configs = json.load(f)

    logging.info("Step 1: Config File has been loaded successfully.")
    print()
except Exception as e:

    error_thrower(1, f"The config file at '{configs_path}' could not be read.")
    raise


########################################
## 2. Reading the final crash records ##
########################################

try:
    crash_dataset_path = configs.get('files_paths').get('ready_crash_dataset')

    crash_records = pd.read_csv(crash_dataset_path)

    logging.info("Step 2: Crash dataset has been read successfully.")
    print()

except:
    error_thrower(2, f"The crash dataset at '{crash_dataset_path}' could not be read.")
    raise


#################################################################
## #. Creating bad weather and bad lighting and road condition ## ================> will move to crash dataset
#################################################################

reason_name_change = {
            'alcohol_or_drug': 'Alcohol or Drug',
            'sleepy_ill_dizzy_driver': 'Sleepy/Ill/Dizzy Driver',
            'Unsafe Speed': 'Speeding',
            'Inattention': 'Distraction'
            }

crash_records = crash_records.rename(columns=reason_name_change)

bad_weather = ['Fog/Smoke', 'Rain', 'Snow', 'Sleet/Hail/Freezing Rain',
               'Severe Crosswind', 'Blowing Snow', 'Blowing Dust/Sand']
crash_records['Bad Weather'] = crash_records['weather_condition'].apply(lambda x: 1 if x in bad_weather else 0)

bad_lighting = ['Dark / Unlighted', 'Dusk', 'Dawn']
crash_records['Bad Lighting'] = crash_records['lighting_condition'].apply(lambda x: 1 if x in bad_lighting else 0)

bad_roadway_condition = range(3, 10)
crash_records['Bad Road Condition'] = crash_records['road_condition'].apply(lambda x: 1 if x in bad_roadway_condition else 0)


#####################################################
## 3. Finding the Involvement of all crash reasons ##
#####################################################

try:
    checkable_crash_reasons = configs.get('checkable_crash_reasons')
    human_related_crash_reasons = configs.get('human_related_crash_reasons')
    all_reasons_involvement_path = configs.get('files_paths').get('all_reasons_involvement_path')

    all_reasons_involvement =  all_reasons_finder(crash_records, checkable_crash_reasons, human_related_crash_reasons)

    all_reasons_involvement.to_csv(all_reasons_involvement_path, index=False)

    logging.info("Step 3: All crashes sole involvement file has been created successfully.")
    print()

except:
    error_thrower(3, f"All crashes sole involvement file could not be created.")
    raise

######################################
## 4. Finding the top crash reasons ##
######################################

try:
    checkable_crash_reasons = configs.get('checkable_crash_reasons')
    reason_consideration_threshold = configs.get('reason_consideration_threshold')
    heatmap_save_main_path = configs.get('files_paths').get('heatmap_save_main_path')
    top_reasons_involvement_path = configs.get('files_paths').get('top_reasons_involvement_path')

    top_reasons_dataframe = top_reasons_finder(crash_records, checkable_crash_reasons, reason_consideration_threshold, heatmap_save_main_path)
    top_reasons_dataframe.to_csv(top_reasons_involvement_path, index=False)
    top_reasons = top_reasons_dataframe['Reason'].tolist()

    logging.info("Step 4: Top crash reasons were found successfully.")
    print()

except:
    error_thrower(4, f"Top crash reasons could not be found.")
    raise



############################################################
## 5. Getting the stats for each of the top crash reasons ##
############################################################

try:
    checkable_crash_types = configs.get('checkable_crash_types')
    crash_type_consideration_threshold = configs.get('crash_type_consideration_threshold')
    reasons_stat_save_main_path = configs.get('files_paths').get('reasons_stat_save_main_path')

    reason_stat_creator(crash_records, top_reasons, checkable_crash_reasons, checkable_crash_types,
                        reason_consideration_threshold, crash_type_consideration_threshold, reasons_stat_save_main_path)

    logging.info("Step 5: Statistics for each crash reason involvement were created successfully.")
    print()

except:
    error_thrower(5, f"Statistics for each crash reason involvement could not be created.")
    raise


###################################################################
## 6. Getting the stats for each of the top crash reasons - ONLY ##
###################################################################

try:
    only_reasons_stat_save_main_path = configs.get('files_paths').get('only_reasons_stat_save_main_path')

    only_reason_stat_creator(crash_records, top_reasons, checkable_crash_reasons, checkable_crash_types, crash_type_consideration_threshold, only_reasons_stat_save_main_path)

    logging.info("Step 6: Statistics for each crash reason ONLY involvement were created successfully.")
    print()

except:
    error_thrower(6, f"Statistics for each crash reason ONLY involvement could not be created.")
    raise

