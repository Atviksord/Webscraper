import asyncio
import requests
from bs4 import BeautifulSoup

link = 'https://www.thesportsdb.com/season/4711-Sumo/2024&r=01'
baselink = 'https://www.thesportsdb.com'

async def scrapeBase():
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
    
    
 





linklist = asyncio.run(scrapeBase())


