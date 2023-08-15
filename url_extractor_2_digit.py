import requests
from bs4 import BeautifulSoup
import json
import os
import re
import pandas as pd

def scrape_table_from_url(url):
    try:
        # Fetch HTML content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Placeholder for our data
        data = []

        # select all table rows where you detect "list_rubri" in an HREF in the row
        table_rows = soup.select('tr:has(a[href*="list_rubri"])')

        for row in table_rows:
            columns = row.select('td')
            
            if len(columns) < 3:  # Check if there are at least 3 columns (Number, Name, Description)
                continue

            number = columns[0].get_text(strip=True) if columns[0] else None
            name = columns[1].get_text(strip=True) if columns[1] else None
            link = columns[1].find('a')['href'] if columns[1].find('a') else None
            description = columns[2].get_text(strip=True) if columns[2] else None

            if number and name and description:
                entry = {
                    "Number": number,
                    "Name": name,
                    "Description (tasks and duties)": description,
                    "Link": f"https://historyofwork.iisg.nl/{link}" if link else None
                }
                data.append(entry)

        # Check and create directory if not exists
        output_dir = "data/occupations"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Extract the digits from the URL
        digits = re.search(r'text01=(\d+)', url)
        if digits:
            digits = digits.group(1)
        else:
            raise ValueError("Unable to extract digits from the URL")


        # File path to save
        file_name = f"hisco_{digits}.json"
        file_path = os.path.join(output_dir, file_name)

        # Save the data as JSON
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        return f"Data saved to {file_path}"

    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# test
url = "https://historyofwork.iisg.nl/list_minor.php?text02=0&&text01_qt=strict"

scrape_table_from_url(url)