import os
import json
import pandas as pd

# Initialize an empty list to hold data from all JSON files
all_data = []

# Path to your directory
dir_path = 'data/occupations'

# Loop through all JSON files
for filename in os.listdir(dir_path):
    if filename.startswith("hisco_") and filename.endswith(".json"):
        file_path = os.path.join(dir_path, filename)
        
        # Open and read the file
        with open(file_path, 'r') as f:
            data = json.load(f)
            all_data.extend(data)

# Convert the list to a DataFrame
df = pd.DataFrame(all_data)

# save the DataFrame as a CSV file to "data/occupations/3-digit-occupations.csv"
df.to_csv('data/occupations/3-digit-occupations.csv', index=False)