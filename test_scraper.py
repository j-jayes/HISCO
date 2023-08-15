import requests
from bs4 import BeautifulSoup
import json

BASE_URL = 'https://historyofwork.iisg.nl/list_rubri.php?keywords=01&keywords_qt=lstrict&orderby=keywords'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

def get_hisco_data(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise ValueError('Failed to retrieve the webpage.')

    soup = BeautifulSoup(response.content, 'html.parser')
    
    data = []
    rows = soup.select('table[border="0"] tr')[1:]  # Excluding the header row

    for row in rows:
        number = row.find('p', class_='rubri_code').text.strip()
        name = row.find('a').text.strip()
        description = row.find_all('td')[2].text.strip()  # The third td in the row
        
        data.append({
            'Number': number,
            'Name': name,
            'Description': description
        })

    return data

def save_to_json(data, filename='hisco_data.json'):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def main():
    data = get_hisco_data(BASE_URL)
    save_to_json(data)

if __name__ == '__main__':
    main()
