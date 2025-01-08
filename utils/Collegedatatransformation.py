import json



# Load the uploaded file's contents

file_path = '/Users/happy/HappyIsCreating/collegevine/College_details_CollegeVine.json'



# Load the JSON data from the file

with open(file_path, 'r') as file:

    colleges_data = json.load(file)



# Template for the JSON format

college_template = {

    "college_id": "",

    "name": "",

    "address": {

        "street": "",

        "city": "",

        "state": "",

        "zip": ""

    },

    "website_url": "",

    "image_url": "",

    "financials": {

        "in_state_tuition": None,

        "out_of_state_tuition": None,

        "room_and_board": None,

        "average_aid": None,

        "net_price": {

            "in_state": None,

            "out_of_state": None

        },

        "pell_grant_percentage": None,

        "scholarship_opportunities": []

    },

    "programs": {

        "majors": [

            {

                "category": "",

                "list": []

            }

        ]

    },

    "admissions": {

        "acceptance_rate": None,

        "average_test_scores": {

            "sat": {

                "reading_writing": None,

                "math": None

            },

            "act": {

                "composite": None

            }

        },

        "application_requirements": [],

        "deadlines": {

            "early_decision": "",

            "regular": ""

        }

    },

    "student_life": {

        "clubs": [],

        "sports": [],

        "facilities": []

    },

    "student_body": {

        "undergraduate_enrollment": None,

        "international_percentage": None,

        "in_state_percentage": None,

        "gender_ratio": {

            "male": None,

            "female": None

        },

        "diversity": {

            "ethnicity": {

                "white": None,

                "black": None,

                "asian": None,

                "hispanic": None,

                "other": None

            }

        }

    },

    "career_outcomes": {

        "average_salary": None,

        "job_placement_rate": None,

        "internship_opportunities": []

    },

    "similar_schools": []

}

# Update the helper function to handle missing 'jsonLd'
def transform_college_data_safe(college_entry):
    transformed = json.loads(json.dumps(college_template))  # Deep copy to avoid mutating the template
    metadata = college_entry.get('metadata', {})
    json_ld = (metadata.get('jsonLd') or [{}])[0]

    transformed["college_id"] = json_ld.get("identifier", "")
    transformed["name"] = json_ld.get("name", "")
    
    address = json_ld.get("address", "")
    if address:
        parts = address.split(", ")
        transformed["address"]["street"] = parts[0] if len(parts) > 0 else ""
        transformed["address"]["city"] = parts[1] if len(parts) > 1 else ""
        state_zip = parts[2] if len(parts) > 2 else ""
        if state_zip:
            state_zip_parts = state_zip.split(" ")
            transformed["address"]["state"] = state_zip_parts[0]
            transformed["address"]["zip"] = state_zip_parts[1] if len(state_zip_parts) > 1 else ""
    
    transformed["website_url"] = metadata.get("canonicalUrl", "")
    # Additional fields remain unprocessed for now due to data constraints
    return transformed

# Process all colleges with updated function
transformed_colleges_safe = [transform_college_data_safe(college) for college in colleges_data]

# Save the transformed data to a new JSON file
output_path_safe = '/Users/happy/HappyIsCreating/collegevine/Transformed_Colleges_Safe.json'
with open(output_path_safe, 'w') as output_file_safe:
    json.dump(transformed_colleges_safe, output_file_safe, indent=4)

output_path_safe
