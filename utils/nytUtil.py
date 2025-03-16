import json
from bs4 import BeautifulSoup
import requests
import re

def getNYTData():
    urlpage = 'https://www.nytimes.com/puzzles/letter-boxed'
    page = requests.get(urlpage)
    # parse the html using beautiful soup and store in variable 'soup'
    soup = BeautifulSoup(page.content, 'html.parser')
    script_tag = soup.find('script', type='text/javascript', string=re.compile('window.gameData'))
    pattern = r'window\.gameData\s*=\s*({[^;]*})'
    contents = re.search(pattern, script_tag.string)
    contents = contents.group(1)
    full_data = json.loads(contents)
    print(full_data['sides'])
    return full_data