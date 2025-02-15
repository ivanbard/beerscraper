#web scraper for the beer store - Ivan Bardziyan
import requests
from bs4 import BeautifulSoup
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

response = requests.get("https://www.thebeerstore.ca/beers", headers=headers)#how about i just change it to either look at lcbo OR check dynamic html

if response.status_code == 200:
    beer_text = response.text
    soup = BeautifulSoup(beer_text, 'lxml')
    print(soup.prettify())
    
    beer_data = soup.find_all('h2')
    beer_list = []
    for beer in beer_data:
        if 'PLP_PRODUCT_ID' in beer.parent.get('id',''):
            beer_list.append(beer.get_text(strip=True))

    if beer_list:
        print(f"Found {len(beer_list)} beers.")
        for name in beer_list[:10]:  # Print first 10 for debugging
            print(name)
    else:
        print('no beer data found.')

else:
    print(f"cant fetch page status code: {response.status_code}")
