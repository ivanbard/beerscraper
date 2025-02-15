# web scraper for the beer store - ivanbard
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

beer_text = requests.get('https://www.thebeerstore.ca/beers', headers=headers).text
soup = BeautifulSoup(beer_text, 'lxml')

if beer_text.status_code == 200:
    soup = BeautifulSoup(beer_text, 'lxml')
    beer_data = soup.find_all('h2')
    if beer_data:
        print(f"Found {len(beer_data)} beers.")
        for beer in beer_data[:10]:
            print(beer.text.strip())
    else:
        print('no beer found')
else:
    print(f'failed to fetch page')

#beer_data = soup.find_all('div', class_="px-[12px] sm:px-[20px] font-sans font-medium text-[14px]")
#print(beer_data) 