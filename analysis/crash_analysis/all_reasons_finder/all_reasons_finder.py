import pandas as pd

def all_reasons_finder(crash_records, checkable_crash_reasons, human_related_crash_reasons):

    # Initialize dictionary to store results
    all_reasons_dict = {'Reason': [], 'Being the Sole Reason (%)': [], 'Human Related': []}

    crash_records_len = crash_records.shape[0]

    for reason in checkable_crash_reasons:
        # Count occurrences where all other crash reasons are 0 for each reason
        reason_count = ((crash_records[checkable_crash_reasons].drop(columns=[reason]) == 0).all(axis=1) & (crash_records[reason] == 1)).sum()
        
        # Calculate percentage
        reason_involvement_perc = round((reason_count / crash_records_len * 100), 2)

        # Append reason, involvement percentage, and whether it's human related
        all_reasons_dict['Reason'].append(reason)
        all_reasons_dict['Being the Sole Reason (%)'].append(reason_involvement_perc)
        all_reasons_dict['Human Related'].append('Yes' if reason in human_related_crash_reasons else 'No')

    # Convert dictionary to DataFrame and sort by involvement percentage
    all_reasons_df = pd.DataFrame(all_reasons_dict).sort_values(by='Being the Sole Reason (%)', ascending=False).reset_index(drop=True)

    return all_reasons_df
