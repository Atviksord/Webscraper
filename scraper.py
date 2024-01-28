import asyncio
import requests
from bs4 import BeautifulSoup
import re

link = 'https://www.thesportsdb.com/season/4711-Sumo/2024&r=01' # change link to suit which tournament
baselink = 'https://www.thesportsdb.com'

async def scrapeBase(): # scrapes the baselink and gets all the links to every day of the tournament
    response = requests.get(link)
    soup = BeautifulSoup(response.text,'html.parser')
    linklist = []
    atags = soup.find_all('a')
    for tag in atags:
        d = tag.get('href')
        if d.startswith('/event'):
            d = (f'{baselink}{d}')
            linklist.append(d)

    
    return linklist
    
async def scrapeTournament(linklist):
    response = requests.get(linklist[0])
    playerlist = []
    soup = BeautifulSoup(response.text,'html.parser')
    tdTags = soup.find_all('tr') #Each TR tag contains each player info, each info is stored in a TD tag
    for tdTag in tdTags:
        playerstring = re.split('(LOSS|WIN|^\d+\s)',tdTag.text)
        completedPlayer = playerstring[1:-1]
        if completedPlayer:
            playerlist.append(completedPlayer)
    
       
    print(playerlist)   



    
    

        

 





linklist = asyncio.run(scrapeBase())
asyncio.run(scrapeTournament(linklist))


