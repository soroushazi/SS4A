import json

import geopandas as gpd

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import logging
logging.basicConfig(level=logging.INFO)


from error_thrower.error_thrower import error_thrower
from intersection_creator.intersection_creator import intersection_creator
from duplicate_remover.duplicate_remover import duplicate_remover


################################
## 1. Reading the Config File ##
################################

try:
    configs_path = 'intersection_dataset/configs/configs.json'
    with open(configs_path, 'r') as f:
        configs = json.load(f)

    logging.info("Step 1: Config File has been loaded successfully.")
    print()
except Exception as e:

    error_thrower(1, f"The file path '{configs_path}' does not exist.")
    raise


#####################################
## 2. Reading the Roadways Network ##
#####################################

def roadway_network_reader():

    try:
        roadway_dataset_path = configs.get('files_paths').get('roadway_network_path')
        roadway_dataset = gpd.read_file(roadway_dataset_path)

        logging.info("Step 2: Config File has been loaded successfully.")
        print()

        return roadway_dataset

    except Exception as e:

        error_thrower(2, f"The file path '{roadway_dataset}' does not exist.")
        raise

# roadway_dataset = roadway_network_reader()

###################################
## 3. Creating the intersections ##
###################################

def intersection_creation(roadway_dataset):

    try:
        # path to save the raw intersections file
        raw_intersections_save_path = configs.get('files_paths').get('new_raw_intersections_save_path')

        raw_intersections = intersection_creator(roadway_dataset, raw_intersections_save_path)

        logging.info("Step 3: Raw intersections file has been created successfully.")
        print()

        return raw_intersections
    except:
        error_thrower(3, f"Raw intersections file could not be created.")
        raise

# raw_intersections = intersection_creation(roadway_dataset)


#######################################################
## 4. Removing the intersections close to each other ##
#######################################################

raw_intersections_save_path = configs.get('files_paths').get('raw_intersections_save_path')
raw_intersections = gpd.read_file(raw_intersections_save_path)

clean_buffer = configs.get('clean_buffer')

intersections_without_duplicate_path = configs.get('files_paths').get('intersections_without_duplicate_path')
projected_crs = configs.get('projected_crs')
duplicate_remover(raw_intersections, clean_buffer, intersections_without_duplicate_path)

