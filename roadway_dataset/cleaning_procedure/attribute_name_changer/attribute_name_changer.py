import json


def attribute_name_changer(roadway_network):
    """
    Renames the columns of a DataFrame using the given mapping.
    
    Parameters:
    roadway_network : pandas.DataFrame
        The DataFrame whose columns need to be renamed.
    attributes_mapping : dict
        A dictionary where the keys are the new column names and the values are the current column names in the DataFrame.
    
    Returns:
    pandas.DataFrame
        A DataFrame with renamed columns.
    """

    # Attributes Names
    configs_path = 'roadway_dataset/configs/configs.json'
    with open(configs_path, 'r') as f:
        configs = json.load(f)

    attributes_mapping = configs.get('attributes_mapping')

    # the mapping the dictionary
    mapping = {k: v for k, v in attributes_mapping.items() if k in roadway_network.columns}

    # Filtering the attributes in the dictionary
    roadway_network = roadway_network[mapping.keys()]
    
    # Rename the columns in the DataFrame
    roadway_network = roadway_network.rename(columns=mapping)
    
    return roadway_network

