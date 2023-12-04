import requests,random
from bs4 import BeautifulSoup
import pandas as pd
from rich.progress import track

BASE_URL = "https://www.leagueofgraphs.com/fr/rankings/summoners/page-"

USER_AGENTS = [ 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
	'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
	'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36' 
]

def get_random_user_agent():
    return random.choice(USER_AGENTS) 


def make_request(url):
    headers = {'User-Agent': get_random_user_agent()} 
    response = requests.get(url,headers=headers)
    if not response.ok:
        raise Exception(f"Request failed with error code {response.status_code}")
    return response.text

names = []
rankings = []
for i in track(range(1,51),"Scraping..."):
    url = BASE_URL + str(i)
    html = make_request(url)
    soup = BeautifulSoup(html,"html.parser")
    table = soup.find("table",class_="summonerRankingsTable")
    trs = table.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        if tds:
            for td in tds:
                div = td.find("div",class_="txt")
                if div:
                    names.append(div.find("span",class_="name").text.strip())
        td = tr.find("td",class_="hide-for-small-down")
        if td: ranking = td.text.strip(); rankings.append(ranking)
        
df = pd.DataFrame({"summoners" : names,"rankings" : rankings})
df.to_csv("df.csv")





