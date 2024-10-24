from attribute_assigner.separate_attribute_assigner.year_assigner import year_assigner
from attribute_assigner.separate_attribute_assigner.crash_type_cleaner import crash_type_cleaner
from attribute_assigner.separate_attribute_assigner.alcohol_or_drug_assigner import alcohol_or_drug_assigner
from attribute_assigner.separate_attribute_assigner.teen_older_driver_assigner import teen_older_driver_assigner
from attribute_assigner.separate_attribute_assigner.id2name_attribute_assigner import attributes_id2name_assigner
from attribute_assigner.separate_attribute_assigner.sleepy_ill_dizzy_driver_assigner import sleepy_ill_dizzy_driver_assigner
from attribute_assigner.separate_attribute_assigner.unsafe_unlaw_id2desc import unsafe_unlaw_id2desc
from attribute_assigner.separate_attribute_assigner.reason_assigner import reason_assigner


def main_attribute_assigner(crash_records):

    """
    Assigns multiple attributes to crash_records DataFrame by chaining different assignment functions.
    """

    # performing each of the assignments as a step
    steps = [year_assigner, crash_type_cleaner, alcohol_or_drug_assigner, teen_older_driver_assigner,
             attributes_id2name_assigner, sleepy_ill_dizzy_driver_assigner, unsafe_unlaw_id2desc, reason_assigner]
    
    for step in steps:
        crash_records = step(crash_records)

    return crash_records
