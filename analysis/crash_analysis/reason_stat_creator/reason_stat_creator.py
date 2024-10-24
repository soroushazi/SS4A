import pandas as pd

import os


def reason_stat_creator(crash_records, top_reasons, all_reasons, checkable_crash_types, reason_consideration_threshold, crash_type_consideration_threshold, reasons_stat_save_main_path):
    
    for reason in top_reasons:

        crash_records_involving_this_reason = crash_records[crash_records[reason] == 1]
        crash_records_involving_this_reason_len = crash_records_involving_this_reason.shape[0]
        crash_records_involving_this_reason_perc = round((crash_records_involving_this_reason_len / crash_records.shape[0] * 100), 2)

        # Finding the top secondary reasons for each specific reason
        other_top_reasons_dict = {}
        crash_records_just_this_reason = crash_records_involving_this_reason.copy()
        for other_reason in all_reasons:
            if other_reason != reason:
                crash_records_just_this_reason = crash_records_just_this_reason[crash_records_just_this_reason[other_reason] == 0]

                crash_records_other_reason_len = crash_records_involving_this_reason[crash_records_involving_this_reason[other_reason] == 1].shape[0]
                crash_records_other_reason_involvemnet = round((crash_records_other_reason_len / crash_records_involving_this_reason_len * 100), 2)
                
                if crash_records_other_reason_involvemnet >= reason_consideration_threshold:
                    other_top_reasons_dict[other_reason] = [crash_records_other_reason_involvemnet]

        other_top_reasons_df = pd.DataFrame(other_top_reasons_dict)

        # Finding the top crash types for each specific reason
        top_involving_crash_types_dict = {}
        for crash_type in checkable_crash_types:
            this_crash_type_len = crash_records_involving_this_reason[crash_records_involving_this_reason['main_crash_type'] == crash_type].shape[0]
            this_crash_type_involvement = round((this_crash_type_len / crash_records_involving_this_reason_len * 100), 2)

            if this_crash_type_involvement >= crash_type_consideration_threshold:
                top_involving_crash_types_dict[crash_type] = [this_crash_type_involvement]
        
        
        crash_types_name_change = {
            'OTHER': 'Other',
            'FIXED-OBJECT': 'Fixed-Object',
            'RIGHT-ANGLE': 'Right-Angle',
            'ANGLE-TURNING': 'Angle-Turning',
            'REAR-END': 'Rear-End',
            'SIDESWIPE-SAME': 'Sideswipe-Same Direction',
            'SIDESWIPE-OPP': 'Sideswipe-Opposite Direction',
            'OTH-BACKING': 'Other Backing',
            'PEDESTRIAN': 'Pedestrian',
            'ROLLOVER': 'Rollover',
            'HEAD-ON': 'Head-On',
            'ANGLE-OTHER': 'Angle-Other',
            'VEH-TRAIN': 'Vehicle-Train',
            'PEDAL-CYCLE': 'Pedal-Cycle',
            'OTH-SINGLE-VEH': 'Other-Single-Vehicle',
            'ANIMAL': 'Animal'
            }

        crash_types_name_change = {k:v for k, v in crash_types_name_change.items() if k in top_involving_crash_types_dict.keys()}
        top_involving_crash_types_df = pd.DataFrame(top_involving_crash_types_dict).rename(columns=crash_types_name_change)


        crash_records_just_this_reason_len = crash_records_just_this_reason.shape[0]
        crash_records_just_this_reason_perc = round((crash_records_just_this_reason_len / crash_records_involving_this_reason_len * 100), 2)

        # Severity level calculator
        severity_level_percs = {}
        for severity_level in crash_records_involving_this_reason['severity_level']:
            this_severity_level_len = crash_records_involving_this_reason[crash_records_involving_this_reason['severity_level'] == severity_level].shape[0]
            this_severity_level_perc = round((this_severity_level_len / crash_records_involving_this_reason_len * 100), 2)
            severity_level_percs[severity_level] = [this_severity_level_perc]
        severity_level_percs_df = pd.DataFrame(severity_level_percs)


        # Driver Age calculator
        teen_driver_len = crash_records_involving_this_reason[crash_records_involving_this_reason['teen_driver'] == 1].shape[0]
        teen_driver_perc = round((teen_driver_len / crash_records_involving_this_reason_len * 100), 2)

        older_driver_len = crash_records_involving_this_reason[crash_records_involving_this_reason['older_driver'] == 1].shape[0]
        older_driver_perc = round((older_driver_len / crash_records_involving_this_reason_len * 100), 2)

        driver_age_df = pd.DataFrame({'Teen Driver': [teen_driver_perc], 'Older Driver': [older_driver_perc]})

        # All together
        reason_stat_dict = {
            'Reason': [reason],
            
            f'All Crashes involved {reason}': [crash_records_involving_this_reason_len], f'All Crashes involved {reason} / All Crashes (%)': [crash_records_involving_this_reason_perc],
            f'Crashes Solely due to {reason}': [crash_records_just_this_reason_len], f'Crashes Solely due to {reason} (%)': [crash_records_just_this_reason_perc]
            }
        
        reason_stat_df = pd.DataFrame(reason_stat_dict)
        
        # Adding the severity levels
        severity_levels_name_change = {
            'fatal': 'Fatal Crashes',
            'incapacitating_injury': 'Incapacitating Injury Crashes',
            'non_incapacitating_injury': 'Non-Incapacitating Injury Crashes',
            'possible_injury': 'Possible Injury Crashes',
            'property_damage': 'Property Damage Crashes'
            }
        reason_stat_df = pd.concat([reason_stat_df, severity_level_percs_df], axis=1).rename(columns=severity_levels_name_change)

        # Adding driver age
        reason_stat_df = pd.concat([reason_stat_df, driver_age_df], axis=1)

        # Adding top secondary reasons
        reason_stat_df = pd.concat([reason_stat_df, other_top_reasons_df], axis=1)

        # Adding top top crash typs
        reason_stat_df = pd.concat([reason_stat_df, top_involving_crash_types_df], axis=1)
        # Always adding pedestrian
        pedestrian_crash_type_len = crash_records_involving_this_reason[crash_records_involving_this_reason['main_crash_type'] == 'PEDESTRIAN'].shape[0]
        pedestrian_crash_type_perc = round((pedestrian_crash_type_len / crash_records_involving_this_reason_len * 100), 2)
        pedestrian_crash_type_df = pd.DataFrame({'Pedestrian': [pedestrian_crash_type_perc]})
        reason_stat_df = pd.concat([reason_stat_df, pedestrian_crash_type_df], axis=1)

        # Saving the dataframe for showing on map and creating the heatmap for each of the crashes
        reason_stat_save_path = os.path.join(reasons_stat_save_main_path, reason)
        if not os.path.isdir(reason_stat_save_path):
            os.makedirs(reason_stat_save_path, exist_ok=True)
        reason_stat_df.to_csv(os.path.join(reason_stat_save_path, f'{reason}.csv'), index=False)

        

