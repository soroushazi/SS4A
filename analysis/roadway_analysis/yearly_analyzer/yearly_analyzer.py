import pandas as pd
import jenkspy
from collections import Counter



def yearly_analyzer(merged_crashes):

    ##### Getting the total number of crashes for each year #####
    # Get a list of all unique roadways and years
    all_roadways = merged_crashes['roadway_index'].unique()
    all_years = merged_crashes['year'].unique()

    # Create a complete set of all roadway and year combinations
    complete_index = pd.MultiIndex.from_product([all_roadways, all_years], names=['roadway_index', 'year'])

    # Get the actual crash counts per roadway and year
    yearly_merged_crashes = merged_crashes.groupby(['roadway_index', 'year']).size().reset_index(name='Total Number of Crashes')

    # Create a DataFrame with all roadway-year combinations
    complete_combinations = pd.DataFrame(index=complete_index).reset_index()

    # Merge the actual crash data with the complete set of roadway/year combinations
    # Fill missing values with 0 for roadways/years without crashes
    yearly_merged_crashes_complete = complete_combinations.merge(
        yearly_merged_crashes, on=['roadway_index', 'year'], how='left').fillna(0)

    # Convert the "Total Number of Crashes" column back to integer
    yearly_merged_crashes_complete['Total Number of Crashes'] = yearly_merged_crashes_complete['Total Number of Crashes'].astype(int)


    ##### Getting the ones that are on top every year #####    
    # Creating the dictionary of number of occurrence in each year
    yearly_tops = {}
    for year in all_years:
        this_year_analysis = yearly_merged_crashes_complete[yearly_merged_crashes_complete['year'] == year]

        total_crashes_values = this_year_analysis['Total Number of Crashes'].values
        total_crashes_breaks = jenkspy.jenks_breaks(total_crashes_values, n_classes=3)

        high_threshold = total_crashes_breaks[2]
        this_years_high = this_year_analysis[this_year_analysis['Total Number of Crashes'] >= high_threshold]['roadway_index'].tolist()

        yearly_tops[year] = this_years_high
        
    # Flatten all roadway_indexs into a single list
    all_yearly_tops = [roadway_index for year, roadways in yearly_tops.items() for roadway_index in roadways]

    # Count occurrences of each roadway_index
    roadway_counts = Counter(all_yearly_tops)

    # Find the roadway_index(s) with the maximum number of occurrences
    max_occurrence = max(roadway_counts.values())
    most_common_roadways = [roadway_index for roadway_index, count in roadway_counts.items() if count == max_occurrence]

    return max_occurrence, most_common_roadways
