import pandas as pd

# Define the column names you want to keep from 'Most-Recent-Cohorts-Institution.csv'
required_columns = [
    "unitid", "OPEID", "OPEID6", "INSTNM", "CITY", "STABBR", "ZIP", "ACCREDAGENCY", "INSTURL",
    "NPCURL", "SCH_DEG", "HCM2", "MAIN", "NUMBRANCH", "PREDDEG", "HIGHDEG", "CONTROL", 
    "ST_FIPS", "REGION", "LOCALE", "LOCALE2", "LATITUDE", "LONGITUDE"
]

# Load only the required columns from 'Most-Recent-Cohorts-Institution.csv'
# Using chunksize to load the file in chunks to handle large files
chunksize = 100000  # Read the file in chunks of 100,000 rows at a time
file_path_most_recent = 'Most-Recent-Cohorts-Institution.csv'
file_path_merged_college = 'merged_college_data.csv'

# Initialize an empty list to hold the chunks of merged data
merged_data = []

# Read the 'merged_college_data.csv' file into a dataframe
merged_college_data = pd.read_csv(file_path_merged_college)

# Iterate over the chunks of 'Most-Recent-Cohorts-Institution.csv'
for chunk in pd.read_csv(file_path_most_recent, usecols=required_columns, chunksize=chunksize):
    # Merge the chunk with the 'merged_college_data' dataframe on 'unitid'
    chunk_merged = pd.merge(chunk, merged_college_data, on="unitid", how="inner")
    # Append the result to the merged_data list
    merged_data.append(chunk_merged)

# Concatenate all the merged chunks into one dataframe
final_merged_data = pd.concat(merged_data, ignore_index=True)

# Write the merged data to a new CSV file
output_file = 'final_merged_college_data_1.csv'
final_merged_data.to_csv(output_file, index=False)

print(f'Merging completed. Data written to {output_file}')

