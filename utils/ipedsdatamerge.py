import pandas as pd

# def merge_college_data(field_of_study_file, file_247, file_302, output_file="merged_college_data.csv"):
def merge_college_data(field_of_study_file, file_247,  output_file="merged_college_data_1.csv"):    
    """Merges college data from three CSV files, including ALL fields, and selects relevant ones for initial display.

    Args:
        field_of_study_file: Path to the field of study CSV file.
        file_247: Path to the CSV_112025-247.csv file.
        file_302: Path to the CSV_112025-302.csv file.
        output_file: Path to the output CSV file.
    """
    try:
        # Read the CSV files into Pandas Dataframes, handling potential errors and large files
        field_of_study_df = pd.read_csv(field_of_study_file, encoding='latin1', low_memory=False)
        df_247 = pd.read_csv(file_247, encoding='latin1', low_memory=False)
       # df_302 = pd.read_csv(file_302, encoding='latin1', low_memory=False)

        # Merge the Dataframes on the `unitid` column, using outer joins to preserve all data
        merged_df = pd.merge(field_of_study_df, df_247, on="unitid", how="outer")
       # merged_df = pd.merge(merged_df, df_302, on="unitid", how="outer")

        # Write ALL columns to the CSV (for complete data storage)
        merged_df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Merged data (ALL fields) saved to {output_file}")

        # Select a subset of relevant fields for initial display and LLM interaction.
        # This keeps the initial data manageable but allows access to all data from the saved CSV.
        relevant_fields = [
            "unitid", "INSTNM", "HD2023.Institution name alias", "HD2023.City location of institution",
            "HD2023.State abbreviation", "HD2023.ZIP code", "CONTROL", "CIPDESC", "CREDDESC",
            "HD2023.Sector of institution", "HD2023.Level of institution", "HD2023.Historically Black College or University",
            "HD2023.Tribal college", "HD2023.Degree of urbanization (Urban-centric locale)", "EARN_MDN_HI_1YR",
            "EARN_MDN_HI_2YR", "DRVGR2023.Graduation rate, total cohort", "DRVADM2023.Percent admitted - total",
            "DRVIC2023.Tuition and fees, 2023-24", "DRVIC2023.Total price for in-state students living on campus 2023-24",
            "DRVIC2023.Total price for out-of-state students living on campus 2023-24",
            "SFA2223.Percent of full-time first-time undergraduates awarded any financial aid",
            "SFA2223.Average amount of federal, state, local or institutional grant aid awarded",
            "SFA2223.Average net price-students awarded grant or scholarship aid, 2022-23", "ADM2023.Secondary school GPA",
            "ADM2023.SAT Evidence-Based Reading and Writing 50th percentile score", "ADM2023.SAT Math 50th percentile score",
            "ADM2023.ACT Composite 50th percentile score", "HD2023.Admissions office web address",
            "IC2023mission.Mission statement", "IC2023mission.Mission statement URL (if mission statement not provided)",
            "HD2023.Online application web address", "HD2023.Net price calculator web address"
        ]
        merged_college_data_display = merged_df[relevant_fields]

        print("Displaying a subset of relevant fields:")
        print(merged_college_data_display.head().to_markdown(index=False, numalign="left", stralign="left"))
        print(merged_college_data_display.info())

    except FileNotFoundError:
        print("Error: One or more input files not found.")
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Example usage (replace with your actual file paths)
field_of_study_file = "data/Most-Recent-Cohorts-Field-of-Study.csv"
file_247 = "data/CSV_112025-972.csv"
file_302 = "data/CSV_112025-280.csv"
file_most_recent_cohort = "Most-Recent-Cohorts-Institution.csv"
merge_college_data("merged_college_data.csv", file_most_recent_cohort)
# merge_college_data(field_of_study_file, file_247, file_302)