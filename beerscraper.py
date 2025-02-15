#web scraper for the beer store - Ivan Bardziyan
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import re, csv

chromedriver_autoinstaller.install()

#selenium options
options = Options()
options.add_argument("--headless") #in background instead of popping up
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("start-maximized")

searched_beer = input("What beer are you looking for? ").strip()
fs_beer = searched_beer.replace(" ", "%20")

driver = webdriver.Chrome(options=options)
url = "https://www.thebeerstore.ca/beers?query=" + fs_beer
driver.get(url) #use the search feature to allow user to search for the beer the desire.
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "lxml")
driver.quit()

beer_data = soup.find_all('div', class_="justify-between text-card-foreground flex info-height flex-col border border-[#D6D6D6] border-solid rounded-[10px] relative shadow-none overflow-hidden clear-both")
beer_list = [beer.get_text(strip=True) for beer in beer_data]
pattern = re.compile(r'^(.*?)\s*(\d{1,3})\s*X\s*(?:Bottle|Can)\s*(\d+\s*ml)\s*\$([\d,.]+)')
structured_beer = []
for beer in beer_list:
    match = pattern.search(beer)
    if match:
        beer_name = match.group(1).strip() 
        pack_size = match.group(2) 
        bottle_size = match.group(3)
        price = match.group(4)

        structured_beer.append([beer_name, pack_size, bottle_size, f"${price}"])

print(f"Found {len(structured_beer)} beers.\n")

for beer in structured_beer:
    print(f"Name: {beer[0]} | Pack Size: {beer[1]} | Bottle Size: {beer[2]} | Price: {beer[3]}")

#csv for storage and processing later
with open("beer_list.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Beer Name", "Pack Size", "Bottle Size", "Price"])
    writer.writerows(structured_beer)

'''
if beer_list:
    print(f"Found {len(beer_list)} beers.")
    for name in beer_list:
        print(name)
else:
    print("No beer data found. Check HTML structure again.")

clean_list = [name.split('*')[0].strip() for name in beer_list]
for name in clean_list:
    print(name)
'''