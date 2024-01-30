import asyncio
import requests
from bs4 import BeautifulSoup
import re
import json

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
    
async def scrapeTournament(linklist,day=0):
    
    playerlist = []
    
    response = requests.get(linklist[day])
    soup = BeautifulSoup(response.text,'html.parser')
    tdTags = soup.find_all('tr') #Each TR tag contains each player info, each info is stored in a TD tag
    for tdTag in tdTags:
        playerstring = re.split('(LOSS|WIN|^\d+\s)',tdTag.text)
        completedPlayer = playerstring[1:-1]
        if completedPlayer:
            playerlist.append(completedPlayer)
    return playerlist
    
    
    
#create logic for the dictionary
def createdic(playerlist, tournament_dict={}, day = 1):
    rikishidictionary = {}  
    for rikishi in playerlist:

        if rikishi[1] in tournament_dict:
            rikishidictionary[rikishi[1]] = dict(tournament_dict[rikishi[1]]) 
        else:        
            rikishidictionary[rikishi[1]] = {'WIN':0,'LOSS':0,'OPPONENT':'','RESULT':rikishi[2]}
    
        if rikishi[2] == 'WIN':
            rikishidictionary[rikishi[1]]['WIN']+= 1
        elif rikishi[2] == 'LOSS':
            rikishidictionary[rikishi[1]]['LOSS']+= 1

    for x in range(len(playerlist)):
        if x < (len(playerlist)-1) and playerlist[x][0] == playerlist[x+1][0]:
            rikishidictionary[playerlist[x][1]]['OPPONENT'] = playerlist[x+1][1]
        if x > 0 and playerlist[x][0] == playerlist[x-1][0]:
            rikishidictionary[playerlist[x][1]]['OPPONENT'] = playerlist[x-1][1]
    return rikishidictionary

def storedata(rikishidictionary):
   with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(rikishidictionary, ensure_ascii=False))

async def main():
    links = await scrapeBase()
    master_dict = {}
    tournament_dict = {}
    for day in range(len(links)):
        playerlist = await scrapeTournament(links,day)
        rikishidictionary = createdic(playerlist, tournament_dict, day+1)
        tournament_dict.update(rikishidictionary)
        master_dict[f'Day {day+1}'] = rikishidictionary
    print('Finished')
    storedata(master_dict)

    

    

asyncio.run(main())
    


