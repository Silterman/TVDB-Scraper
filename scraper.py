from bs4 import BeautifulSoup as BS
import requests
import os

link = "https://thetvdb.com/series/uncoupled/allseasons/official"
dest = "B:\\Emby\\Downloads\\Uncoupled\\"
#
startSeason = 0 #this is techically 1 due to list indexing
numSeasons = 1

page = requests.get(link)
soup = BS(page.content, "html.parser") #grabs entire page HTML and turns it into some sort of class

#Creates a list entry for each UL. 
#TVDB has a UL for each season in HTML. This is also causing problems with single season shows as it does not use a UL in the HTML.
seasons = soup.find_all('ul',attrs={"class" : "list-group"})

def createSeasonDictionary(season: list) -> dict:    
    episodeTitleBundle = {}

    #Creates a new list with each entry being a string containing the season, episode number and title.
    episodes = [name.get_text().strip() for name in season.find_all("h4", attrs={"class": "list-group-item-heading"}) if name.get_text().strip() != ""]
    #Removes specials from this list due incompatibility, might look into supporting them later
    episodes = [episode for episode in episodes if 'SPECIAL' not in episode]
    
    for i in range(len(episodes)):
        #.split entry might need to be made dynamic, but it's not resulted in an error so far
        episodes[i] = episodes[i].replace("\n", "").split("                                    ")
        #using a lot of replaces to remove forbidden file characters
        episodeTitleBundle.update({episodes[i][0][episodes[i][0].index("E"):]:episodes[i][1].replace("?", "").replace("|", "").replace(":", "").replace("*", "").replace("<", "").replace(">", "").replace('"', "")})
    return episodeTitleBundle

def replaceFilenames(seasonNum: int, episodeTitleBundle: dict) -> None:
    destLocal = dest + f"Season {seasonNum}\\"
    for file in os.listdir(destLocal):
        if file[:file.index(".")] in episodeTitleBundle:
            print(f"Renaming {file} to {file[:file.index('.')]+' '+episodeTitleBundle[file[:file.index('.')]]+file[file.index('.'):]} in {destLocal}")
            os.rename(destLocal+file ,destLocal+file[:file.index(".")]+" "+episodeTitleBundle[file[:file.index(".")]]+file[file.index("."):])
    

for season in range(len(seasons[startSeason:numSeasons])):
    seasonDictionary = createSeasonDictionary(seasons[season])
    replaceFilenames(season+1, seasonDictionary)