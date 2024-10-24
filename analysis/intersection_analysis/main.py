import json

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import geopandas as gpd

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
    configs_path = 'analysis/intersection_analysis/configs/configs.json'
    with open(configs_path, 'r') as f:
        configs = json.load(f)

    logging.info("Step 1: Config File has been loaded successfully.")
    print()
except Exception as e:

    error_thrower(1, f"The config file at '{configs_path}' could not be read.")
    raise


#######################################
## 2. Reading the Intersections File ##
#######################################

try:
    intersections_dataset_path = configs.get('files_paths').get('intersections_dataset_path')
    intersections = gpd.read_file(intersections_dataset_path)

    logging.info(f"Step 2: Intersections file could be read at `{intersections_dataset_path}` successfully.")
    print()
except Exception as e:

    error_thrower(2, f"Intersections file could not be read at `{intersections_dataset_path}`.")
    raise


#################################
## 3. Reading the Crashes File ##
#################################

try:
    crashes_dataset_path = configs.get('files_paths').get('crashes_dataset_path')
    crashes = gpd.read_file(crashes_dataset_path)
    crashes = crashes[crashes['intersection_rel'] == '1']

    logging.info(f"Step 3: Crashes file could be read at `{crashes_dataset_path}` successfully.")
    print()
except Exception as e:

    error_thrower(3, f"Crashes file could not be read at `{crashes_dataset_path}`.")
    raise


###########################################
## 4. Merging Crashes with Intersections ##
###########################################

try:
    epsg = configs.get('epsg')
    projected_crs = configs.get('projected_crs')
    intersection_buffer = configs.get('intersection_buffer')
    merged_crashes_with_intersections_path = configs.get('files_paths').get('merged_crashes_with_intersections_path')

    merged_crashes = get_crashes_within_radius(crashes, intersections, intersection_buffer, epsg, projected_crs)
    merged_crashes = merged_crashes.rename(columns={
        'index_right': 'intersection_index',
        'FID': 'intersection_id',
        'geometry': 'intersection_location'
        })

    merged_crashes.to_csv(merged_crashes_with_intersections_path, index=False)

    logging.info(f"Step 4: Intersection merge with crashes got saved to `{merged_crashes_with_intersections_path}` successfully.")
    print()
except Exception as e:

    error_thrower(4, f"Intersection merge with crashes could not be saved.")
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

        intersections_epdo = crash_rate_calculator(merged_crashes, epdo_rates, all_severity_levels, number_of_epdo_categories)
        # Saving as csv
        intersections_epdo.to_csv(total_crash_rates_csv_path, index=False)
        # Saving as shp
        intersections_epdo.to_file(total_crash_rates_shp_path)

        logging.info(f"Step 5: IntersectionEPDO values for intersections got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(5, f"EPDO values for intersections could not be calculated.")
        raise

# all_crash_rates_calculator_for_all_reasons()


##############################
## 6. Calculate Crash Rates ## => HIN
##############################

def hin_calculator_for_all_reasons():
    try:
        HIN_crash_rates_csv_path = configs.get('files_paths').get('HIN_crash_rates_csv_path')
        HIN_crash_rates_shp_path = configs.get('files_paths').get('HIN_crash_rates_shp_path')
        # For HIN severity levels => No Property Damage
        HIN_severity_levels = ['fatal', 'incapacitating_injury', 'non_incapacitating_injury', 'possible_injury']

        HIN_intersections_epdo = crash_rate_calculator(merged_crashes, epdo_rates, HIN_severity_levels, number_of_epdo_categories)
        # Saving as csv
        HIN_intersections_epdo.to_csv(HIN_crash_rates_csv_path, index=False)
        # Saving as shp
        HIN_intersections_epdo.to_file(HIN_crash_rates_shp_path)

        logging.info(f"Step 6: HIN EPDO values for intersections got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(6, f"HIN EPDO values for intersections could not be calculated.")
        raise

# hin_calculator_for_all_reasons()


################################################
## 7. Calculating crash rates for each reason ## => All
################################################

def all_crash_rates_calculator_for_each_reason():
    try:

        print("Wokring on All crashes rates")

        main_reasons_crash_datasets_path = configs.get('files_paths').get('main_reasons_crash_datasets_path')

        main_reasons_total_crash_rates_csv_path = configs.get('files_paths').get('main_reasons_total_crash_rates_csv_path')
        main_reasons_total_crash_rates_shp_path = configs.get('files_paths').get('main_reasons_total_crash_rates_shp_path')

        for root, dirs, files in os.walk(main_reasons_crash_datasets_path, topdown=False):
            for file_path in files:

                reason_name = file_path.split('.')[0]
                file_path = os.path.join(root, file_path)

                print(f"Working on: {reason_name}")

                crashes_with_this_reason = gpd.read_file(file_path)

                merged_crashes_with_this_reason = get_crashes_within_radius(crashes_with_this_reason, intersections, intersection_buffer, epsg, projected_crs)
                merged_crashes_with_this_reason = merged_crashes_with_this_reason.rename(columns={
                    'index_right': 'intersection_index',
                    'FID': 'intersection_id',
                    'geometry': 'intersection_location'
                    })

                intersections_epdo_with_this_reason= crash_rate_calculator(merged_crashes_with_this_reason, epdo_rates,
                                                                        all_severity_levels, number_of_epdo_categories)
                
                # Save as csv
                this_reasons_total_crash_rates_csv_path = os.path.join(main_reasons_total_crash_rates_csv_path, reason_name)
                if not os.path.isdir(this_reasons_total_crash_rates_csv_path):
                    os.makedirs(this_reasons_total_crash_rates_csv_path, exist_ok=True)
                intersections_epdo_with_this_reason.to_csv(f"{this_reasons_total_crash_rates_csv_path}/{reason_name}.csv", index=False)
                # Save as shp
                this_reasons_total_crash_rates_shp_path = os.path.join(main_reasons_total_crash_rates_shp_path, reason_name)
                if not os.path.isdir(this_reasons_total_crash_rates_shp_path):
                    os.makedirs(this_reasons_total_crash_rates_shp_path, exist_ok=True)
                intersections_epdo_with_this_reason.to_file(f"{this_reasons_total_crash_rates_shp_path}/{reason_name}.shp")

        logging.info(f"Step 7: EPDO values for intersections for each reason got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(7, f"EPDO values for intersections for each reason could not be calculated.")
        raise

# all_crash_rates_calculator_for_each_reason()


################################################
## 8. Calculating crash rates for each reason ## => HIN
################################################

def hin_calculator_for_each_reason():
    try:

        print("Wokring on HIN")

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

                merged_crashes_with_this_reason = get_crashes_within_radius(crashes_with_this_reason, intersections, intersection_buffer, epsg, projected_crs)
                merged_crashes_with_this_reason = merged_crashes_with_this_reason.rename(columns={
                    'index_right': 'intersection_index',
                    'FID': 'intersection_id',
                    'geometry': 'intersection_location'
                    })

                intersections_epdo_with_this_reason= crash_rate_calculator(merged_crashes_with_this_reason, epdo_rates,
                                                                        HIN_severity_levels, number_of_epdo_categories)
                
                # Save as csv
                this_reasons_HIN_crash_rates_csv_path = os.path.join(main_reasons_HIN_crash_rates_csv_path, reason_name)
                if not os.path.isdir(this_reasons_HIN_crash_rates_csv_path):
                    os.makedirs(this_reasons_HIN_crash_rates_csv_path, exist_ok=True)
                intersections_epdo_with_this_reason.to_csv(f"{this_reasons_HIN_crash_rates_csv_path}/{reason_name}.csv", index=False)
                # Save as shp
                this_reasons_HIN_crash_rates_shp_path = os.path.join(main_reasons_HIN_crash_rates_shp_path, reason_name)
                if not os.path.isdir(this_reasons_HIN_crash_rates_shp_path):
                    os.makedirs(this_reasons_HIN_crash_rates_shp_path, exist_ok=True)
                intersections_epdo_with_this_reason.to_file(f"{this_reasons_HIN_crash_rates_shp_path}/{reason_name}.shp")

        logging.info(f"Step 8: HIN EPDO values for intersections for each reason got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(8, f"HIN EPDO values for intersections for each reason could not be calculated.")
        raise

# hin_calculator_for_each_reason()


########################
## 9. Yearly Analyzor ##
########################

def yearly_analyzor():
    print('Doing Yearly Analysis')

    try:
        high_yearly_intersection_occurrences_csv_path = configs.get('files_paths').get('high_yearly_intersection_occurrences_csv_path')
        high_yearly_intersection_occurrences_shp_path = configs.get('files_paths').get('high_yearly_intersection_occurrences_shp_path')

        max_occurrence, yearly_merged_crashes = yearly_analyzer(merged_crashes)

        print(f"Highest number of occurrences: {max_occurrence}")
        high_yearly_intersection_occurrences =  merged_crashes[merged_crashes['intersection_id'].isin(yearly_merged_crashes)]

        # Save as csv
        high_yearly_intersection_occurrences.to_csv(high_yearly_intersection_occurrences_csv_path, index=False)
        # Save as shp
        high_yearly_intersection_occurrences_shapefile = high_yearly_intersection_occurrences.groupby('intersection_id')['intersection_location'].first().reset_index()
        high_yearly_intersection_occurrences_shapefile.to_file(high_yearly_intersection_occurrences_shp_path)

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
        # Saving as shp
        total_crashes_all_reason.to_file(total_crashes_shp_path)

        logging.info(f"Step 10: Total number of crashes for intersections got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(10, f"Total number of crashes for intersections could not be calculated.")
        raise

# total_crash_analyzor_all_reasons()


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

                merged_crashes_with_this_reason = get_crashes_within_radius(crashes_with_this_reason, intersections, intersection_buffer, epsg, projected_crs)
                merged_crashes_with_this_reason = merged_crashes_with_this_reason.rename(columns={
                    'index_right': 'intersection_index',
                    'FID': 'intersection_id',
                    'geometry': 'intersection_location'
                    })

                intersections_total_crashes_with_this_reason = total_crashes_counter(merged_crashes_with_this_reason, number_of_categories)

                # Save as csv
                this_reasons_total_crashes_csv_path = os.path.join(main_reasons_total_crashes_csv_path, reason_name)
                if not os.path.isdir(this_reasons_total_crashes_csv_path):
                    os.makedirs(this_reasons_total_crashes_csv_path, exist_ok=True)
                intersections_total_crashes_with_this_reason.to_csv(f"{this_reasons_total_crashes_csv_path}/{reason_name}.csv", index=False)
                # Save as shp
                this_reasons_total_crashes_shp_path = os.path.join(main_reasons_total_crashes_shp_path, reason_name)
                if not os.path.isdir(this_reasons_total_crashes_shp_path):
                    os.makedirs(this_reasons_total_crashes_shp_path, exist_ok=True)
                intersections_total_crashes_with_this_reason.to_file(f"{this_reasons_total_crashes_shp_path}/{reason_name}.shp")

        logging.info(f"Step 11: Total number of crashes for intersections for each reason got calculated successfully.")
        print()
    except Exception as e:

        error_thrower(11, f"Total number of crashes for intersections for each reason could not be calculated.")
        raise

# total_crash_analyzor_each_reason()