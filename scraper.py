from bs4 import BeautifulSoup as BS
import requests
import csv

link = "https://thetvdb.com/series/house/allseasons/official"
page = requests.get(link)

soup = BS(page.content, "html.parser") #grabs entire page HTML and turns it into some sort of class

seasons = soup.find_all('ul',attrs={"class" : "list-group"})
#print(seasons)

def findSeasonEpisodes(season, n):
    if len(n) == 1:
        n = "0" + n
    output = {}
    episodesBundle = [name.get_text().strip() for name in season.find_all("h4", attrs={"class": "list-group-item-heading"}) if name.get_text().strip() != ""]
    episodes = [episode for episode in episodesBundle if 'SPECIAL' not in episode]
    for i in range(len(episodes)):
        tempEpisode = episodes[i].replace("\n", "").split("                                    ")
        episodes[i] = tempEpisode
        output.update({episodes[i][0][episodes[i][0].index("E"):]:episodes[i][1]})
    print(n ,output)
    return output

for i in range(len(seasons))[:-1]:
    findSeasonEpisodes(seasons[i], str(i+1))