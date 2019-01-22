import requests
import json
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import pandas as pd
import numpy as np
import mechanicalsoup
import re

# cleaning/readying our patent_data file
open('patent_data.json', 'w').close()

# get random user agent 
def get_random_ua():
    random_ua = ''
    ua_file = 'user-agents.txt'
    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_ua = lines[int(idx)]
    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_ua.rstrip()

# create random user_agent
user_agent = get_random_ua()

# headers if required
headers = {
    'user-agent': user_agent,
    'referer': 'https://google.com'
    }

patent_numbers = 'patent-numbers.txt'
# num = "7867948"

# returns patent data after submitting search query for the patent number
def form_submit(num): 
    url = "http://patft.uspto.gov/netahtml/PTO/srchnum.htm"

    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},  # Use the lxml HTML parser
        raise_on_404=True,
        user_agent=user_agent,
    )
    browser.open(url)

    browser.select_form()

    #browser.get_current_form().print_summary()

    browser["TERM1"] = num

    response = browser.submit_selected()

    soup = BeautifulSoup(response.content, 'html.parser')

    meta = soup.find("meta")
    
    # patent result page
    res_url = "http://patft.uspto.gov" + meta['content'][6:]

    browser.open(res_url)

    page = browser.get_current_page()

    # extracting the title
    fonts = page.find_all("font")
    title = fonts[3].get_text().rstrip()

    # extracting the abstract
    paras = page.find_all("p")
    abstract = " ".join(paras[0].get_text().split())

    tables = page.find_all("table")
    data = {}
    keys = tables[3].find_all("th")
    vals = tables[3].find_all("td")

    for k,v in zip(keys,vals):
        key = " ".join(k.get_text().split()).replace(":","")
        val = " ".join(v.get_text().split())
        data.update({key : val})

    browser.close()

    return data


patents = []
# looping through all patent numbers to extract and store relevant data in JSON file
with open(patent_numbers) as f:
    for line in f:
        if line != '\n':
            num = line.rstrip()
            print(num)
            patent_data = form_submit(num)
            patents.append({num : patent_data})
            with open('patent_data.json', 'w') as f:  
                json.dump(patents, f)
        else:
            continue