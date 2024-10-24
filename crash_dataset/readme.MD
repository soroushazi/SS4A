
# Overview

This section outlines the necessary steps and checks for the data cleaning process, as well as guidelines for working with configuration files.

---

## What to Check and/or Change

- **Config Files**:
    - Only modify the content of the configuration files, **do not** change the file names or their locations. Altering the names or locations will cause errors in the process since the paths are hardcoded in the code.

---

## Cleaning Process

1. **Reading the Dataset**:  
   The dataset is loaded from the `raw_datasets` folder. The path to this folder is specified in the config files and read by the code.

2. **Reading the Study Boundary**:  
   The study area boundary file is also loaded from the `raw_datasets` folder. The path to this file is retrieved from the config files in the same manner as the dataset.

3. **Executing the Cleaning Process**:  
   The data cleaning steps, as defined in the `cleaning_procedure` folder, are applied to the dataset. These steps include filtering and transforming the data based on specific rules.

4. **Saving the Final Dataset**:  
   The cleaned dataset is saved in the `final_datasets` folder. The destination path for saving the cleaned data is also specified in the config files.

