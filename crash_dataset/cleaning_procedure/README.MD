
# Data Cleaning Process

The data cleaning process is structured in a series of steps to ensure accurate and efficient preparation of the crash records for analysis.

## Steps

### 1. Severity Level Cleanup
Crash records that do not have the desired severity levels (1 and 5) are removed. Since severity level is a critical aspect of the analysis, it is essential to filter out irrelevant records early in the process.
- **Why is this done first?**  
  By removing unnecessary records upfront, we avoid performing further analysis on data that won't be used, reducing the overall processing load.

### 2. In-Boundary Filter
Only crash records that fall within the study area are retained.
- **Why is this necessary?**  
  Location data often contains errors or discrepancies, such as missing (`NaN`) values or points outside the study boundary. Filtering these out ensures that we only work with valid and relevant location data.

### 3. Attribute Name Standardization
Some attribute names are unclear or contain special characters and spaces, which complicates handling them in dataframes.
- **Why is this important?**  
  Renaming attributes to be more descriptive and consistent makes it easier to work with the data programmatically and ensures better readability.

### 4. Attribute Assignment
- Many attributes are coded, and we need to convert these codes into descriptive labels to make the data more straightforward.
- Additional columns are created based on existing data. For example, we create an "Old Driver" column by checking the driver’s age and categorizing them appropriately.
  
### 5. Region Assignment
Based on the counties, a region column is added for further analysis.
- **Why is this necessary?**  
  Region-based analysis requires assigning crash records to specific regions defined by the counties.

### 6. Tulsa Urban Region Assignment
For Cherokee Nation’s SS4A analysis, we specifically assign the Tulsa Urban region to the dataset.
- **Why this region?**  
  This step is required due to the specific focus of the analysis on the Cherokee Nation.

### 7. Saving the Clean Dataset
After cleaning, only the columns needed for further analysis are saved.
- **Why focus on certain columns?**  
  This helps streamline subsequent analysis by keeping only the relevant data and reducing the dataset size.

---

## Notes

1. Each step is handled in its own file, except for the Attribute Assignment step. Since Attribute Assignment involves multiple sub-steps, it is separated for better error handling and modularity.
  
2. The `main.py` script integrates all the steps to process the data in sequence.

