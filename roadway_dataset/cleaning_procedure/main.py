import json

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import logging
logging.basicConfig(level=logging.INFO)


from out_bounday_remover.out_bounday_remover import out_boundary_remover
from attribute_name_changer.attribute_name_changer import attribute_name_changer
from attributes_code2desc.attributes_code2desc import attributes_code2desc_assigner
from two_roadway_networks_merger.two_roadway_networks_merger import two_roadway_networks_merger
from error_thrower.error_thrower import error_thrower

################################
## 1. Reading the Config File ##
################################

try:
    configs_path = 'roadway_dataset/configs/configs.json'
    with open(configs_path, 'r') as f:
        configs = json.load(f)

    datasets_path = configs.get('files_paths')

    logging.info("Step 1: Config File has been loaded successfully.\n")
except Exception:
    error_thrower(1, f"The file path '{configs_path}' does not exist.")


###########################################################################
## 2. Removing the roadway network that is outside of the study boundary ##
###########################################################################

# raw_roadway_datasets_path = datasets_path.get('raw_roadway_datasets_path')

# raw_datasets = {}
# for root, dirs, files in os.walk(raw_roadway_datasets_path):
#     for file in files:
#         if file.endswith('.shp'):
#             file_name = file.split('.')[0]
#             raw_datasets[file_name] = os.path.join(root, file)



##### Main Roadway Network #####
try:
    # Reading the files
    main_roadway_network_path = datasets_path.get('main_roadway_network_path')
    study_boundary_path = datasets_path.get('study_boundary_path')
    cleaned_main_roadway_network_path = datasets_path.get('main_roadway_network_path')

    epsg = configs.get('epsg')

    main_roadway_network = out_boundary_remover(main_roadway_network_path, study_boundary_path, epsg, cleaned_main_roadway_network_path)

    logging.info("Step 2: Main Roadway Network outside of the boundaries has been removed successfully.")
except Exception:
    error_thrower(2, f"Main Roadway Network outside of the boundaries could not be removed.")

##### Local Roadway Network #####
try:
    local_roadway_network_path = datasets_path.get('local_roadway_network_path')
    cleaned_local_roadway_network_path = datasets_path.get('cleaned_local_roadway_network_path')

    local_roadway_network = out_boundary_remover(local_roadway_network_path, study_boundary_path, epsg, cleaned_local_roadway_network_path)

    logging.info("Step 2: Road Roadway Network outside of the boundaries has been removed successfully.\n")
    print()
except Exception:
    error_thrower(2, f"Local Roadway Network outside of the boundaries could not be removed.")


# ##########################################################################
# ## Step 3: Filtering only the attributes wanted and changing their name ##
# ##########################################################################


# try:
#     main_roadway_network = attribute_name_changer(main_roadway_network)

#     logging.info("Step 3: Main Roadway Network got filtered successfully.")
# except Exception as e:
#     error_thrower(3, "Main Roadway could not get filtered.")

# try:
#     local_roadway_network = attribute_name_changer(local_roadway_network)

#     logging.info("Step 3: Local Roadway Network got filtered successfully.\n")
# except Exception as e:
#     error_thrower(3, "Local Roadway could not get filtered.")


# ########################################
# ## 4. Attributes Codes to Description ##
# ########################################

# try:
#     main_roadway_network = attributes_code2desc_assigner(main_roadway_network)

#     logging.info("Step 4: Main Roadway Network attributes converted from code to description successfully.")
# except Exception as e:
#     error_thrower(4, "Main Roadway Network attributes converted from code to description could not be done.")

# try:
#     local_roadway_network = attributes_code2desc_assigner(local_roadway_network)

#     logging.info("Step 4: Local Roadway Network attributes converted from code to description successfully.\n")
#     print()
# except Exception as e:
#     error_thrower(4, "Local Roadway Network attributes converted from code to description could not be done.")

# ###################################################
# ## 5. Merging the two different roadway networks ##
# ###################################################

# try:
#     if sorted(main_roadway_network.columns) != sorted(local_roadway_network.columns):
#         error_thrower(5, "The attributes for the two roadway networks are not the same.")

#     combined_roadway = two_roadway_networks_merger("main", main_roadway_network, "local", local_roadway_network)

#     logging.info("Step 5: The two roadway networks got merged successfully.\n")

# except Exception as e:
#     error_thrower(5, "The two roadway networks could not get merged.")


# #################################
# ## 6. Saving the final dataset ##
# #################################

# try:
#     final_roadway_network_path = datasets_path.get('final_roadway_network_path')
#     combined_roadway.to_file(final_roadway_network_path)
    
#     logging.info(f"Step 6: The final roadway network got saved in `{final_roadway_network_path}` successfully.\n")

# except Exception:
#     error_thrower(6, "The final roadway network could not get saved.")

