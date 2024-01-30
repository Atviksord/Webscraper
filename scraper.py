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
def createdic(playerlist,rikishidictionary = {},day = 1):
    
    for rikishi in playerlist:
        if rikishi[1] not in rikishidictionary:
            rikishidictionary.update({rikishi[1]:{'WIN':0,'LOSS':0,'OPPONENT':'','BOUTNUMBER':rikishi[0]}})
    for rikishi in playerlist:
        if rikishi[2] == 'WIN':
            rikishidictionary[rikishi[1]]['WIN']+= 1
        elif rikishi[2] == 'LOSS':
            rikishidictionary[rikishi[1]]['LOSS']+= 1
    for x in range(len(playerlist)):
        if x < (len(playerlist)-1) and playerlist[x][0] == playerlist[x+1][0]:
            rikishidictionary[playerlist[x][1]]['OPPONENT'] = playerlist[x+1][1]
        if x > 0 and playerlist[x][0] == playerlist[x-1][0]:
            rikishidictionary[playerlist[x][1]]['OPPONENT'] = playerlist[x-1][1]
    return {f'Day {day}':rikishidictionary},rikishidictionary   

def storedata(rikishidictionary):
   with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(rikishidictionary, ensure_ascii=False))

async def main():
    links = await scrapeBase()
    master_dict = {}
    for day in range(15):
         playerlist = await scrapeTournament(links,day)
         day_dict,dic = createdic(playerlist)
         master_dict.update(day_dict)
    print('Finished')
    storedata(master_dict)
    

    

asyncio.run(main())
    

        




#linklist = asyncio.run(scrapeBase())
#asyncio.run(scrapeTournament(linklist))


