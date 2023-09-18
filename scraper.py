from bs4 import BeautifulSoup as BS
import requests
import os

link = "https://thetvdb.com/series/house/allseasons/official"
#link = "https://thetvdb.com/series/the-mentalist/allseasons/official"

numSeasons = 8

page = requests.get(link)

dest = "B:\\Emby\\Series\\House\\"

soup = BS(page.content, "html.parser") #grabs entire page HTML and turns it into some sort of class

seasons = soup.find_all('ul',attrs={"class" : "list-group"})
#print(seasons)

def findSeasonEpisodes(season, n):
    destLocal = dest + f"Season {n}\\"
    output = {}
    episodesBundle = [name.get_text().strip() for name in season.find_all("h4", attrs={"class": "list-group-item-heading"}) if name.get_text().strip() != ""]
    episodes = [episode for episode in episodesBundle if 'SPECIAL' not in episode]
    for i in range(len(episodes)):
        tempEpisode = episodes[i].replace("\n", "").split("                                    ")
        episodes[i] = tempEpisode
        #using a lot of replaces to remove forbidden file characters
        output.update({episodes[i][0][episodes[i][0].index("E"):]:episodes[i][1].replace("?", "").replace("|", "").replace(":", "").replace("*", "").replace("<", "").replace(">", "").replace('"', "")})
    #print(output)
    for file in os.listdir(destLocal):
        if file[:file.index(".")] in output:
            print(f"Renaming {file} to {file[:file.index('.')]+' '+output[file[:file.index('.')]]+file[file.index('.'):]} in {destLocal}")
            os.rename(destLocal+file ,destLocal+file[:file.index(".")]+" "+output[file[:file.index(".")]]+file[file.index("."):])
    return output

for i in range(len(seasons[:numSeasons])):
    findSeasonEpisodes(seasons[i], str(i+1))