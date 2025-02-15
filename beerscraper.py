#web scraper for the beer store - Ivan Bardziyan
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

#selenium options
options = Options()
options.add_argument("--headless") #in background instead of popping up
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("start-maximized")

driver = webdriver.Chrome(options=options)
driver.get("https://www.thebeerstore.ca/beers")
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "lxml")

driver.quit()

beer_data = soup.find_all('div', class_="justify-between text-card-foreground flex info-height flex-col border border-[#D6D6D6] border-solid rounded-[10px] relative shadow-none overflow-hidden clear-both")
beer_list = [beer.get_text(strip=True) for beer in beer_data]
'''
if beer_list:
    print(f"Found {len(beer_list)} beers.")
    for name in beer_list:
        print(name)
else:
    print("No beer data found. Check HTML structure again.")
'''

clean_list = [name.split('*')[0].strip() for name in beer_list]
for name in clean_list:
    print(name)
