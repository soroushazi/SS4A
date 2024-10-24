import json
import pandas as pd

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


import logging
logging.basicConfig(level=logging.INFO)

from attribute_name_changer.attribute_name_changer import attribute_name_changer
from severity_level_cleaner.severity_level_cleaner import severity_level_cleaner
from out_boundary_remover.out_boundary_remover import out_boundary_remover
from attribute_assigner.main_attribute_assigner import main_attribute_assigner
from attribute_assigner.separate_attribute_assigner.region_assigner import region_assigner
from tulsa_region_assigner.tulsa_region_assigner import tulsa_region_assigner
from focused_column_cleaner.focused_column_cleaner import focused_column_cleaner
from error_thrower.error_thrower import error_thrower

#############################
## Step 1: Reading Configs ##
#############################

try:
    configs_path = 'crash_dataset/configs/configs.json'
    with open(configs_path, 'r') as f:
        configs = json.load(f)

    # Files paths
    datasets_path = configs.get('files_paths')

    logging.info("Step 1: Configs file was read successfully.\n")
except:
    error_thrower(2, f"The file path at `{configs_path}` could not be read.")


###################################
## Step 2: Reading Crash Dataset ##
###################################

try:
    # Getting the crash records file path
    crash_records_file_path = datasets_path.get('crash_records_file_path')

    # Reading the crash records file
    crash_records = pd.read_csv(crash_records_file_path, low_memory=False)

    logging.info("Step 2: Crash Records have been read successfully.\n")
except:
    print("Step 2: Crash Records could not be read.")
    raise


######################################################
## Step 3: Changing the attributes names to desired ##
######################################################

try:
    # Reading the attributes_names_path
    attributes_names = configs.get('attributes_names')

    crash_records = attribute_name_changer(crash_records, attributes_names)
    logging.info("Step 3: The name of the attributes have been changed successfully.\n")
except:
    logging.info("Step 3: The name of the attributes could not be changed.")
    raise


####################################################
## Step 4: Removing the incorrect severity levels ##
####################################################

try:
    # Reading the acceptable severity levels
    acceptable_severity_levels = configs.get('acceptable_severity_levels')

    unique_crash_records = severity_level_cleaner(crash_records, attributes_names, acceptable_severity_levels)
    logging.info("Step 4: The desired severity levels have been filtered successfully.\n")
except:
    logging.info("Step 4: The desired severity levels could not be filtered.")
    raise


################################################################
## Step 5: Removing the Records outside of the Study Boundary ##
################################################################

try:
    # Reading the path to study area file
    study_area_file_path = datasets_path.get('study_area_file_path')
    # Reading the epsg
    epsg = configs.get('epsg')

    # Doing the thing
    unique_crash_records = out_boundary_remover(unique_crash_records, study_area_file_path, attributes_names, epsg)
    logging.info("Step 5: The crash records outside of the study area have been removed successfully.\n")
except:
    logging.info("Step 5: The crash records outside of the study area could not be removed.")
    raise


#########################################
## Step 6: Assigning Crash Attributes  ##
#########################################

try:
    unique_crash_records = main_attribute_assigner(unique_crash_records)
    logging.info("Step 6: The attribute assignemnt completed successfully.\n")
except:
    logging.info("Step 6: The attribute assignemnt could not be done.")
    raise


###############################
## Step 7: Assgining Regions ##
###############################

try:
    # Reading the regions_dict
    regions = configs.get('regions')

    unique_crash_records = region_assigner(unique_crash_records, attributes_names, regions)

    logging.info("Step 7: The region assignment completed successfully.\n")
except:
    logging.info("Step 7: The region assignment could not be done.")
    raise


####################################
## Step 8: Assgining Tulsa Region ##
####################################

try:
    # Reading the shapefile for Tulsa
    tulsa_urban_area_file_path = datasets_path.get('tulsa_urban_area_file_path')

    unique_crash_records = tulsa_region_assigner(unique_crash_records, attributes_names, tulsa_urban_area_file_path, epsg)
    logging.info("Step 8: The Tulsa region assignment completed successfully.\n")
except:
    logging.info("Step 8: The Tulsa region assignment could not be done.")
    raise


#############################################
## Step 9: Getting Only Desired Attributes ##
#############################################

try:

    # Reading the focused columns
    focused_columns = configs.get('focused_columns')

    unique_crash_records = focused_column_cleaner(unique_crash_records, focused_columns)
    logging.info("Step 9: The focused columns have been filtered successfully.\n")
except:
    logging.info("Step 9: The focused columns filtering could not be done.")
    raise


#######################################
## Step 10: Saving the Final Dataset ##
#######################################

try:
    final_dataset_path = datasets_path.get('final_dataset_path')
    unique_crash_records.to_csv(final_dataset_path, index=False)
    logging.info("Step 10: The final dataset has been saved successfully.\n")
except:
    logging.info("Step 10: The final dataset could not be saved.")
    raise


