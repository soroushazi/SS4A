import json

def attributes_code2desc_assigner(roadway_network):

    # Getting the attributes id to names dictionary
    configs_path = 'roadway_dataset/configs/configs.json'
    with open(configs_path, 'r') as f:
        configs = json.load(f)

    attributes_code2desc_dict = configs.get('attributes_code2desc')

    for category, attribute_dict in attributes_code2desc_dict.items():

        # because we are reading json file and json keys cannot be int => need to change the category to int (because some are float) then to str and then map
        roadway_network[category] = roadway_network[category].astype(str)
        roadway_network[category] = roadway_network[category].map(attribute_dict)

    return roadway_network

