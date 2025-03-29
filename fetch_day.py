import json
import os
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

JSON_FILE = "nyt_data.json"
def fetchToday():
    #key returns: ourSolution, dictionary, isNYT
    urlpage = 'https://www.nytimes.com/puzzles/letter-boxed'
    page = requests.get(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page.content, 'html.parser')
    script_tag = soup.find('script', type='text/javascript', string=re.compile('window.gameData'))
    pattern = r'window\.gameData\s*=\s*({[^;]*})'
    contents = re.search(pattern, script_tag.string)
    contents = contents.group(1)
    full_data = json.loads(contents)
    out_data = {
        "sides" : full_data['sides'],
        "outSolution" : full_data['ourSolution'],
        "dictionary" : full_data['dictionary']
        }
    return full_data['printDate'] , out_data


if __name__ == "__main__":
    # Load existing data if available
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = {}  # Handle potential corruption gracefully
    else:
        all_data = {}

    # Fetch new data
    date, new_data = fetchToday()

    # Append to dictionary
    if date not in all_data:  # Avoid duplicate entries
        all_data[date] = new_data

        # Save back to JSON
        with open(JSON_FILE, "w") as f:
            json.dump(all_data, f, indent=4)

        print(f"Added NYT data for {date}.")
    else:
        print(f"Data for {date} already exists. Skipping update.")
