import requests
from bs4 import BeautifulSoup
from robobrowser import RoboBrowser
import pandas as pd
import numpy as np

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

user_agent = get_random_ua()

headers = {
    'user-agent': user_agent,
    'referer': 'https://google.com'
    }

'''Create RoboBrowser object
   This will act similarly to a typical web browser'''
browser = RoboBrowser(history=True, user_agent=user_agent)

'''Navigate browser to Wunderground's historical weather page'''
browser.open('http://patft.uspto.gov/netahtml/PTO/srchnum.htm')

forms = browser.get_forms()

print(forms)


page = requests.get("http://patft.uspto.gov/netahtml/PTO/srchnum.htm", headers=headers)

# print(page.status_code)

# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())


# def getTitle(url):
#     try:
#         html = urlopen(url)
#     except HTTPError as e:
#         return None
#     try:
#         bsObj = BeautifulSoup(html.read(), features="html.parser")
#         title = bsObj.body.h1
#     except AttributeError as e:
#         return None
#     return title

# url = "http://www.pythonscraping.com/pages/warandpeace.html"
# html = urlopen(url)
# print(html.read())

#title = getTitle(url_var)

# if title == None:
#     print("Title could not be found")
# else:
#     print(title)
