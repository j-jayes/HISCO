# Get 3 digit hisco information

# source the function `scrape_table_from_url` from url_extractor_3_digit.py
from url_extractor_3_digit import scrape_table_from_url

for i in range(1, 100):
    # Convert the number to a 2-digit string with leading zeros
    dd = f"{i:02}"
    url = f"https://historyofwork.iisg.nl/list_rubri.php?keywords={dd}&keywords_qt=lstrict&orderby=keywords"
    scrape_table_from_url(url)