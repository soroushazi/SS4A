import json
from out_boundary_remover.out_boundary_remover import out_boundary_remover


def tulsa_region_assigner(crash_records, attributes_names, tulsa_urban_area_file_path, epsg):

    crash_id_column_name = attributes_names.get('Doc ID')
    region_column_name = attributes_names.get('region')

    tulsa_urban_area_crashes = out_boundary_remover(crash_records, tulsa_urban_area_file_path, attributes_names, epsg)
    tulsa_urban_area_crashes_ids = tulsa_urban_area_crashes[crash_id_column_name].tolist()


    crash_records[region_column_name] = crash_records.apply(lambda row: 'tulsa' if row[crash_id_column_name] in tulsa_urban_area_crashes_ids
                                                                        else row[region_column_name], axis=1)
    
    return crash_records