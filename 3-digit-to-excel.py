import pandas as pd
import os
import json

# Directory where the JSON files are located
directory = 'data/occupations/'

# Initialize an empty list to store the data
data = []

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        # Create the full file path
        filepath = os.path.join(directory, filename)
        
        # Read the JSON file
        with open(filepath, 'r') as file:
            content = json.load(file)
            
            # Append the data to the list
            data.extend(content)

# Create a DataFrame from the list of data
df = pd.DataFrame(data)

# Convert column headers to snake case
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Save the DataFrame to an Excel file
df.to_excel('occupations.xlsx', index=False)
