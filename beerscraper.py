#web scraper for the beer store - Ivan Bardziyan
import time, re, csv, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

def calculate(pack, bottle, price):
    pack_size = int(pack)
    bottle_size = int(bottle.replace("ml", "").strip())
    price = float(price.replace("$", "").strip())

    total = pack_size*bottle_size
    value = total/price if price > 0 else 0
    return round(value, 2)

def sort_by_val(beer_csv):
    beers = []
    with open(beer_csv, "r", encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)

        for row in reader:
            beer_name, pack_size, bottle_size, price, ml_dol = row
            ml_dol= float(ml_dol)
            beers.append([beer_name, pack_size, bottle_size, price, ml_dol])
        
    beers.sort(key=lambda x: x[4], reverse = True) #sort by ml_dol values highest first
    for beer in beers:
        print(f"Name: {beer[0]} | Pack: {beer[1]} | Size: {beer[2]} | Price: {beer[3]} | ml/$: {beer[4]}")
    best = beers[0]
    print("\nBest Value Beer")
    print(f"Name: {best[0]}")
    print(f"Pack Size: {best[1]}")
    print(f"Bottle Size: {best[2]}")
    print(f"Price: {best[3]}")
    print(f"ml/$: {best[4]}")
    return beers

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
driver.get(url)
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
        ml_dol = calculate(pack_size,bottle_size,price)
        structured_beer.append([beer_name, pack_size, bottle_size, f"${price}", ml_dol])

print(f"Found {len(structured_beer)} beers.\n")

for beer in structured_beer:
    print(f"Name: {beer[0]} | Pack Size: {beer[1]} | Bottle Size: {beer[2]} | Price: {beer[3]} | ml/$: {beer[4]}")

#csv for storage and processing later
with open("beer_list.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Beer Name", "Pack Size", "Bottle Size", "Price", "ml per $"])
    writer.writerows(structured_beer)

sort_by_val("beer_list.csv")