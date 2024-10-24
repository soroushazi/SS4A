import os

import pandas as pd



def top_reasons_finder(crash_records, checkable_crash_reasons, reason_consideration_threshold, heatmap_save_main_path):

    crash_records_len = crash_records.shape[0]
    top_reasons_dict = {'Reason': [], 'Involvement Percentage': []}

    for reason in checkable_crash_reasons:
        reason_len = crash_records[crash_records[reason] == 1].shape[0]
        reason_involvement_perc = round((reason_len / crash_records_len * 100), 2)

        if reason_involvement_perc >= reason_consideration_threshold:

            top_reasons_dict['Reason'].append(reason)
            top_reasons_dict['Involvement Percentage'].append(reason_involvement_perc)

            # Saving the dataframe for showing on map and creating the heatmap for each of the crashes
            reason_heatmap_save_path = os.path.join(heatmap_save_main_path, reason)
            if not os.path.isdir(reason_heatmap_save_path):
                os.makedirs(reason_heatmap_save_path, exist_ok=True)

            crash_records[crash_records[reason] == 1].to_csv(os.path.join(reason_heatmap_save_path, f'{reason}.csv'), index=False)

    top_reasons_df = pd.DataFrame(top_reasons_dict).sort_values(by='Involvement Percentage', ascending=False).reset_index(drop=True)
    return top_reasons_df