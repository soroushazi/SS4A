import json

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import geopandas as gpd
import pandas as pd

import logging
logging.basicConfig(level=logging.INFO)

from get_crashes_within_radius.get_crashes_within_radius import get_crashes_within_radius
from crash_rate_calculator.crash_rate_calculator import crash_rate_calculator
from yearly_analyzer.yearly_analyzer import yearly_analyzer
from total_crashes_counter.total_crashes_counter import total_crashes_counter
from error_thrower.error_thrower import error_thrower


################################
## 1. Reading the Config File ##
################################

try:
    configs_path = 'analysis/roadway_analysis/configs/configs.json'
    with open(configs_path, 'r') as f:
        configs = json.load(f)

    logging.info("Step 1: Config File has been loaded successfully.")
    print()
except Exception as e:

    error_thrower(1, f"The config file at '{configs_path}' could not be read.")
    raise


#######################################
## 2. Reading the Roadways File ##
#######################################

try:
    roadways_dataset_path = configs.get('files_paths').get('roadways_dataset_path')
    roadways = gpd.read_file(roadways_dataset_path)
    roadways = roadways[roadways['aadt'] != 0]

    logging.info(f"Step 2: Roadways file was read at `{roadways_dataset_path}` successfully.")
    print()
except Exception as e:

    error_thrower(2, f"Roadways file could not be read at `{roadways_dataset_path}`.")
    raise


#################################
## 3. Reading the Crashes File ##
#################################

try:
    crashes_dataset_path = configs.get('files_paths').get('crashes_dataset_path')
    crashes = gpd.read_file(crashes_dataset_path)
    crashes = crashes[crashes['intersection_rel'] == '0']

    logging.info(f"Step 3: Crashes file was read at `{crashes_dataset_path}` successfully.")
    print()
except Exception as e:

    error_thrower(3, f"Crashes file could not be read at `{crashes_dataset_path}`.")
    raise


######################################
## 4. Merging Crashes with Roadways ##
######################################

try:
    epsg = configs.get('epsg')
    projected_crs = configs.get('projected_crs')
    roadway_buffer = configs.get('roadway_buffer')
    merged_crashes_with_roadway_path = configs.get('files_paths').get('merged_crashes_with_roadway_path')

    merged_crashes = get_crashes_within_radius(crashes, roadways, roadway_buffer, epsg, projected_crs)
    merged_crashes = merged_crashes.rename(columns={
        'index_right': 'roadway_index',
        'FID': 'roadway_id',
        'geometry': 'geometry'
        })

    merged_crashes.to_csv(merged_crashes_with_roadway_path, index=False)

    logging.info(f"Step 4: Roadways merge with crashes got saved to `{merged_crashes_with_roadway_path}` successfully.")
    print()
except Exception as e:

    error_thrower(4, f"Roadways merge with crashes could not be saved.")
    raise


##############################
## 5. Calculate Crash Rates ## => All
##############################

def all_crash_rates_calculator_for_all_reasons():
    try:

        epdo_rates = configs.get('epdo_rates')
        number_of_epdo_categories = configs.get('number_of_epdo_categories')
        total_crash_rates_csv_path = configs.get('files_paths').get('total_crash_rates_csv_path')
        total_crash_rates_shp_path = configs.get('files_paths').get('total_crash_rates_shp_path')
        # For all crashes => all severity levels
        all_severity_levels = merged_crashes['severity_level'].unique().tolist()

        roadways_epdo = crash_rate_calculator(merged_crashes, epdo_rates, all_severity_levels, number_of_epdo_categories)
        # Saving as csv
        roadways_epdo.to_csv(total_crash_rates_csv_path, index=False)
        # Saving as shp
        roadway_epdo_high_epdo_ids = roadways_epdo[roadways_epdo['epdo_group'] == 'High']['roadway_index'].unique().tolist()
        roadways_epdo_high_shapefile = roadways[roadways.index.isin(roadway_epdo_high_epdo_ids)]
        roadways_epdo_high_shapefile['epdo_group'] = 'High'

        roadway_epdo_medium_epdo_ids = roadways_epdo[roadways_epdo['epdo_group'] == 'Medium']['roadway_index'].unique().tolist()
        roadways_epdo_medium_shapefile = roadways[roadways.index.isin(roadway_epdo_medium_epdo_ids)]
        roadways_epdo_medium_shapefile['epdo_group'] = 'Medium'

        roadway_epdo_low_epdo_ids = roadways_epdo[roadways_epdo['epdo_group'] == 'Low']['roadway_index'].unique().tolist()
        roadways_epdo_low_shapefile = roadways[roadways.index.isin(roadway_epdo_low_epdo_ids)]
        roadways_epdo_low_shapefile['epdo_group'] = 'Low'

        roadways_epdo_combined = pd.concat([roadways_epdo_high_shapefile, roadways_epdo_medium_shapefile, roadways_epdo_low_shapefile], ignore_index=True)
        roadways_epdo_combined.to_file(total_crash_rates_shp_path)

        logging.info(f"Step 5: EPDO values for roadways got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(5, f"EPDO values for roadways could not be calculated.")
        raise

# all_crash_rates_calculator_for_all_reasons()


##############################
## 6. Calculate Crash Rates ## => HIN
##############################

def hin_calculator_for_all_reasons():
    try:

        epdo_rates = configs.get('epdo_rates')
        number_of_epdo_categories = configs.get('number_of_epdo_categories')
        HIN_crash_rates_csv_path = configs.get('files_paths').get('HIN_crash_rates_csv_path')
        HIN_crash_rates_shp_path = configs.get('files_paths').get('HIN_crash_rates_shp_path')
        # For HIN severity levels => No Property Damage
        HIN_severity_levels = ['fatal', 'incapacitating_injury', 'non_incapacitating_injury', 'possible_injury']

        HIN_roadways_epdo = crash_rate_calculator(merged_crashes, epdo_rates, HIN_severity_levels, number_of_epdo_categories)
        # Saving as csv
        HIN_roadways_epdo.to_csv(HIN_crash_rates_csv_path, index=False)
        # Saving as shp
        roadway_epdo_high_epdo_ids = HIN_roadways_epdo[HIN_roadways_epdo['epdo_group'] == 'High']['roadway_index'].unique().tolist()
        roadways_epdo_high_shapefile = roadways[roadways.index.isin(roadway_epdo_high_epdo_ids)]
        roadways_epdo_high_shapefile['epdo_group'] = 'High'

        roadway_epdo_medium_epdo_ids = HIN_roadways_epdo[HIN_roadways_epdo['epdo_group'] == 'Medium']['roadway_index'].unique().tolist()
        roadways_epdo_medium_shapefile = roadways[roadways.index.isin(roadway_epdo_medium_epdo_ids)]
        roadways_epdo_medium_shapefile['epdo_group'] = 'Medium'

        roadway_epdo_low_epdo_ids = HIN_roadways_epdo[HIN_roadways_epdo['epdo_group'] == 'Low']['roadway_index'].unique().tolist()
        roadways_epdo_low_shapefile = roadways[roadways.index.isin(roadway_epdo_low_epdo_ids)]
        roadways_epdo_low_shapefile['epdo_group'] = 'Low'

        roadways_epdo_combined = pd.concat([roadways_epdo_high_shapefile, roadways_epdo_medium_shapefile, roadways_epdo_low_shapefile], ignore_index=True)
        roadways_epdo_combined.to_file(HIN_crash_rates_shp_path)

        logging.info(f"Step 6: HIN EPDO values for roadways got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(6, f"HIN EPDO values for roadways could not be calculated.")
        raise

# hin_calculator_for_all_reasons()


################################################
## 7. Calculating crash rates for each reason ## => All
################################################

def all_crash_rates_calculator_for_each_reason():
    try:

        print("Wokring on All crashes rates")

        epdo_rates = configs.get('epdo_rates')
        number_of_epdo_categories = configs.get('number_of_epdo_categories')
        # For all crashes => all severity levels
        all_severity_levels = merged_crashes['severity_level'].unique().tolist()

        main_reasons_crash_datasets_path = configs.get('files_paths').get('main_reasons_crash_datasets_path')

        main_reasons_total_crash_rates_csv_path = configs.get('files_paths').get('main_reasons_total_crash_rates_csv_path')
        main_reasons_total_crash_rates_shp_path = configs.get('files_paths').get('main_reasons_total_crash_rates_shp_path')

        for root, dirs, files in os.walk(main_reasons_crash_datasets_path, topdown=False):
            for file_path in files:

                reason_name = file_path.split('.')[0]
                file_path = os.path.join(root, file_path)

                print(f"Working on: {reason_name}")

                crashes_with_this_reason = gpd.read_file(file_path)

                merged_crashes_with_this_reason = get_crashes_within_radius(crashes_with_this_reason, roadways, roadway_buffer, epsg, projected_crs)
                merged_crashes_with_this_reason = merged_crashes_with_this_reason.rename(columns={
                    'index_right': 'roadway_index',
                    'FID': 'roadway_id',
                    'geometry': 'geometry'
                    })

                roadways_epdo_with_this_reason= crash_rate_calculator(merged_crashes_with_this_reason, epdo_rates,
                                                                        all_severity_levels, number_of_epdo_categories)
                
                # Save as csv
                this_reasons_total_crash_rates_csv_path = os.path.join(main_reasons_total_crash_rates_csv_path, reason_name)
                if not os.path.isdir(this_reasons_total_crash_rates_csv_path):
                    os.makedirs(this_reasons_total_crash_rates_csv_path, exist_ok=True)
                roadways_epdo_with_this_reason.to_csv(f"{this_reasons_total_crash_rates_csv_path}/{reason_name}.csv", index=False)
                # Save as shp
                this_reasons_total_crash_rates_shp_path = os.path.join(main_reasons_total_crash_rates_shp_path, reason_name)
                if not os.path.isdir(this_reasons_total_crash_rates_shp_path):
                    os.makedirs(this_reasons_total_crash_rates_shp_path, exist_ok=True)

                roadway_epdo_high_epdo_ids = roadways_epdo_with_this_reason[roadways_epdo_with_this_reason['epdo_group'] == 'High']['roadway_index'].unique().tolist()
                roadways_epdo_high_shapefile = roadways[roadways.index.isin(roadway_epdo_high_epdo_ids)]
                roadways_epdo_high_shapefile.loc[:, 'epdo_group'] = 'High'

                roadway_epdo_medium_epdo_ids = roadways_epdo_with_this_reason[roadways_epdo_with_this_reason['epdo_group'] == 'Medium']['roadway_index'].unique().tolist()
                roadways_epdo_medium_shapefile = roadways[roadways.index.isin(roadway_epdo_medium_epdo_ids)]
                roadways_epdo_medium_shapefile.loc[:, 'epdo_group'] = 'Medium'

                roadway_epdo_low_epdo_ids = roadways_epdo_with_this_reason[roadways_epdo_with_this_reason['epdo_group'] == 'Low']['roadway_index'].unique().tolist()
                roadways_epdo_low_shapefile = roadways[roadways.index.isin(roadway_epdo_low_epdo_ids)]
                roadways_epdo_low_shapefile.loc[:, 'epdo_group'] = 'Low'

                roadways_epdo_combined = pd.concat([roadways_epdo_high_shapefile, roadways_epdo_medium_shapefile, roadways_epdo_low_shapefile], ignore_index=True)
                roadways_epdo_combined.to_file(f"{this_reasons_total_crash_rates_shp_path}/{reason_name}.shp")

        logging.info(f"Step 7: EPDO values for roadways for each reason got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(7, f"EPDO values for roadways for each reason could not be calculated.")
        raise

# all_crash_rates_calculator_for_each_reason()


################################################
## 8. Calculating crash rates for each reason ## => HIN
################################################

def hin_calculator_for_each_reason():
    try:

        print("Wokring on HIN")

        epdo_rates = configs.get('epdo_rates')
        number_of_epdo_categories = configs.get('number_of_epdo_categories')
        main_reasons_crash_datasets_path = configs.get('files_paths').get('main_reasons_crash_datasets_path')

        main_reasons_HIN_crash_rates_csv_path = configs.get('files_paths').get('main_reasons_HIN_crash_rates_csv_path')
        main_reasons_HIN_crash_rates_shp_path = configs.get('files_paths').get('main_reasons_HIN_crash_rates_shp_path')

        # For HIN severity levels => No Property Damage
        HIN_severity_levels = ['fatal', 'incapacitating_injury', 'non_incapacitating_injury', 'possible_injury']

        for root, dirs, files in os.walk(main_reasons_crash_datasets_path, topdown=False):
            for file_path in files:

                reason_name = file_path.split('.')[0]
                file_path = os.path.join(root, file_path)

                print(f"Working on: {reason_name}")

                crashes_with_this_reason = gpd.read_file(file_path)

                merged_crashes_with_this_reason = get_crashes_within_radius(crashes_with_this_reason, roadways, roadway_buffer, epsg, projected_crs)
                merged_crashes_with_this_reason = merged_crashes_with_this_reason.rename(columns={
                    'index_right': 'roadway_index',
                    'FID': 'roadway_id',
                    'geometry': 'geometry'
                    })

                roadways_epdo_with_this_reason= crash_rate_calculator(merged_crashes_with_this_reason, epdo_rates,
                                                                        HIN_severity_levels, number_of_epdo_categories)
                
                # Save as csv
                this_reasons_HIN_crash_rates_csv_path = os.path.join(main_reasons_HIN_crash_rates_csv_path, reason_name)
                if not os.path.isdir(this_reasons_HIN_crash_rates_csv_path):
                    os.makedirs(this_reasons_HIN_crash_rates_csv_path, exist_ok=True)
                roadways_epdo_with_this_reason.to_csv(f"{this_reasons_HIN_crash_rates_csv_path}/{reason_name}.csv", index=False)
                # Save as shp
                this_reasons_HIN_crash_rates_shp_path = os.path.join(main_reasons_HIN_crash_rates_shp_path, reason_name)
                if not os.path.isdir(this_reasons_HIN_crash_rates_shp_path):
                    os.makedirs(this_reasons_HIN_crash_rates_shp_path, exist_ok=True)

                roadway_epdo_high_epdo_ids = roadways_epdo_with_this_reason[roadways_epdo_with_this_reason['epdo_group'] == 'High']['roadway_index'].unique().tolist()
                roadways_epdo_high_shapefile = roadways[roadways.index.isin(roadway_epdo_high_epdo_ids)]
                roadways_epdo_high_shapefile.loc[:, 'epdo_group'] = 'High'

                roadway_epdo_medium_epdo_ids = roadways_epdo_with_this_reason[roadways_epdo_with_this_reason['epdo_group'] == 'Medium']['roadway_index'].unique().tolist()
                roadways_epdo_medium_shapefile = roadways[roadways.index.isin(roadway_epdo_medium_epdo_ids)]
                roadways_epdo_medium_shapefile.loc[:, 'epdo_group'] = 'Medium'

                roadway_epdo_low_epdo_ids = roadways_epdo_with_this_reason[roadways_epdo_with_this_reason['epdo_group'] == 'Low']['roadway_index'].unique().tolist()
                roadways_epdo_low_shapefile = roadways[roadways.index.isin(roadway_epdo_low_epdo_ids)]
                roadways_epdo_low_shapefile.loc[:, 'epdo_group'] = 'Low'

                roadways_epdo_combined = pd.concat([roadways_epdo_high_shapefile, roadways_epdo_medium_shapefile, roadways_epdo_low_shapefile], ignore_index=True)
                roadways_epdo_combined.to_file(f"{this_reasons_HIN_crash_rates_shp_path}/{reason_name}.shp")

        logging.info(f"Step 8: HIN EPDO values for roadways for each reason got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(8, f"HIN EPDO values for roadways for each reason could not be calculated.")
        raise

# hin_calculator_for_each_reason()


########################
## 9. Yearly Analyzor ##
########################


def yearly_analyzor():
    print('Doing Yearly Analysis')

    try:
        high_yearly_roadway_occurrences_csv_path = configs.get('files_paths').get('high_yearly_roadway_occurrences_csv_path')
        high_yearly_roadway_occurrences_shp_path = configs.get('files_paths').get('high_yearly_roadway_occurrences_shp_path')

        max_occurrence, most_common_roadways = yearly_analyzer(merged_crashes)

        print(f"Highest number of occurrences: {max_occurrence}")
        high_yearly_roadway_occurrences =  roadways[roadways.index.isin(most_common_roadways)]

        # Save as csv
        high_yearly_roadway_occurrences.to_csv(high_yearly_roadway_occurrences_csv_path, index=False)
        # Save as shp
        high_yearly_roadway_occurrences.to_file(high_yearly_roadway_occurrences_shp_path)

        logging.info(f"Step 9: Yearly presence analysis has been done successfully successfully.")
        print()
    except Exception as e:
        error_thrower(9, f"Yearly presence analysis could not be done.")
        raise

# yearly_analyzor()


#############################################
## 10. Total crash analyzor => all reasons ##
#############################################

def total_crash_analyzor_all_reasons():
    try:
        total_crashes_csv_path = configs.get('files_paths').get('total_crashes_csv_path')
        total_crashes_shp_path = configs.get('files_paths').get('total_crashes_shp_path')

        number_of_categories = configs.get('number_of_epdo_categories')

        total_crashes_all_reason = total_crashes_counter(merged_crashes, number_of_categories)
        # Saving as csv
        total_crashes_all_reason.to_csv(total_crashes_csv_path, index=False)
        # Save as shp
        roadway_epdo_high_epdo_ids = total_crashes_all_reason[total_crashes_all_reason['group'] == 'High']['roadway_index'].unique().tolist()
        roadways_epdo_high_shapefile = roadways[roadways.index.isin(roadway_epdo_high_epdo_ids)]
        roadways_epdo_high_shapefile.loc[:, 'group'] = 'High'

        roadway_epdo_medium_epdo_ids = total_crashes_all_reason[total_crashes_all_reason['group'] == 'Medium']['roadway_index'].unique().tolist()
        roadways_epdo_medium_shapefile = roadways[roadways.index.isin(roadway_epdo_medium_epdo_ids)]
        roadways_epdo_medium_shapefile.loc[:, 'group'] = 'Medium'

        roadway_epdo_low_epdo_ids = total_crashes_all_reason[total_crashes_all_reason['group'] == 'Low']['roadway_index'].unique().tolist()
        roadways_epdo_low_shapefile = roadways[roadways.index.isin(roadway_epdo_low_epdo_ids)]
        roadways_epdo_low_shapefile.loc[:, 'group'] = 'Low'

        roadways_epdo_combined = pd.concat([roadways_epdo_high_shapefile, roadways_epdo_medium_shapefile, roadways_epdo_low_shapefile], ignore_index=True)
        roadways_epdo_combined.to_file(total_crashes_shp_path)

        logging.info(f"Step 10: Total number of crashes for roadways got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(10, f"Total number of crashes for roadways could not be calculated.")
        raise

total_crash_analyzor_all_reasons()


#############################################
## 11. Total crash analyzor => each reason ##
#############################################


def total_crash_analyzor_each_reason():
    try:

        print("Wokring on total crash counts")

        main_reasons_crash_datasets_path = configs.get('files_paths').get('main_reasons_crash_datasets_path')

        main_reasons_total_crashes_csv_path = configs.get('files_paths').get('main_reasons_total_crashes_csv_path')
        main_reasons_total_crashes_shp_path = configs.get('files_paths').get('main_reasons_total_crashes_shp_path')

        number_of_categories = configs.get('number_of_epdo_categories')

        for root, dirs, files in os.walk(main_reasons_crash_datasets_path, topdown=False):
            for file_path in files:

                reason_name = file_path.split('.')[0]
                file_path = os.path.join(root, file_path)

                print(f"Working on: {reason_name}")

                crashes_with_this_reason = gpd.read_file(file_path)

                merged_crashes_with_this_reason = get_crashes_within_radius(crashes_with_this_reason, roadways, roadway_buffer, epsg, projected_crs)
                merged_crashes_with_this_reason = merged_crashes_with_this_reason.rename(columns={
                    'index_right': 'roadway_index',
                    'FID': 'roadway_id',
                    'geometry': 'geometry'
                    })

                roadways_total_crashes_with_this_reason = total_crashes_counter(merged_crashes_with_this_reason, number_of_categories)

                # Save as csv
                this_reasons_total_crashes_csv_path = os.path.join(main_reasons_total_crashes_csv_path, reason_name)
                if not os.path.isdir(this_reasons_total_crashes_csv_path):
                    os.makedirs(this_reasons_total_crashes_csv_path, exist_ok=True)
                roadways_total_crashes_with_this_reason.to_csv(f"{this_reasons_total_crashes_csv_path}/{reason_name}.csv", index=False)
                # Save as shp
                this_reasons_total_crashes_shp_path = os.path.join(main_reasons_total_crashes_shp_path, reason_name)
                if not os.path.isdir(this_reasons_total_crashes_shp_path):
                    os.makedirs(this_reasons_total_crashes_shp_path, exist_ok=True)
                roadway_epdo_high_epdo_ids = roadways_total_crashes_with_this_reason[roadways_total_crashes_with_this_reason['group'] == 'High']['roadway_index'].unique().tolist()
                roadways_epdo_high_shapefile = roadways[roadways.index.isin(roadway_epdo_high_epdo_ids)]
                roadways_epdo_high_shapefile.loc[:, 'group'] = 'High'

                roadway_epdo_medium_epdo_ids = roadways_total_crashes_with_this_reason[roadways_total_crashes_with_this_reason['group'] == 'Medium']['roadway_index'].unique().tolist()
                roadways_epdo_medium_shapefile = roadways[roadways.index.isin(roadway_epdo_medium_epdo_ids)]
                roadways_epdo_medium_shapefile.loc[:, 'group'] = 'Medium'

                roadway_epdo_low_epdo_ids = roadways_total_crashes_with_this_reason[roadways_total_crashes_with_this_reason['group'] == 'Low']['roadway_index'].unique().tolist()
                roadways_epdo_low_shapefile = roadways[roadways.index.isin(roadway_epdo_low_epdo_ids)]
                roadways_epdo_low_shapefile.loc[:, 'group'] = 'Low'
                print(roadways_epdo_low_shapefile.shape[0])

                roadways_epdo_combined = pd.concat([roadways_epdo_high_shapefile, roadways_epdo_medium_shapefile, roadways_epdo_low_shapefile], ignore_index=True)
                roadways_epdo_combined.to_file(f"{this_reasons_total_crashes_shp_path}/{reason_name}.shp")

        logging.info(f"Step 11: Total number of crashes for roadways for each reason got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(11, f"Total number of crashes for roadways for each reason could not be calculated.")
        raise

total_crash_analyzor_each_reason()
