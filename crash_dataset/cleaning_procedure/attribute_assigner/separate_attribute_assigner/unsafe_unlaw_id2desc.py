import json


def unsafe_unlaw_id2desc(crash_records):
    """
    Takes a DataFrame and adds two new columns: 'unsafe_unlaw_category' and 'unsafe_unlaw_desc',
    based on the 'unsafe_unlaw_id' column and the provided traffic violations data.
    
    Parameters:
    crash_records : pandas.DataFrame
        The Unique Crash Records DataFrame
    
    Returns:
    pandas.DataFrame
        The original DataFrame with two new columns: 'unsafe_unlaw_category' and 'unsafe_unlaw_desc'.
    """

    # Getting the unsafe/unlaw actions dict
    configs_path = 'crash_dataset/configs/configs.json' 
    with open(configs_path, 'r') as f:
        configs = json.load(f)
    unsafe_unlaw_actions_dict = configs.get('unsafe_unlaw_actions')

    # Convert the JSON data to a dictionary for fast lookup
    id_to_data = {item['id']: (item['category'], item['description']) for item in unsafe_unlaw_actions_dict}
    
    # Define functions to get the category and description based on the id
    def get_category(unsafe_unlaw_id):
        return id_to_data.get(unsafe_unlaw_id, (None, None))[0]
    
    def get_desc(unsafe_unlaw_id):
        return id_to_data.get(unsafe_unlaw_id, (None, None))[1]

    # Create the two new columns by applying the functions to 'unsafe_unlaw_id'
    crash_records['unsafe_unlaw_category'] = crash_records['unsafe_unlaw_id'].apply(get_category)
    crash_records['unsafe_unlaw_desc'] = crash_records['unsafe_unlaw_id'].apply(get_desc)
    
    return crash_records

