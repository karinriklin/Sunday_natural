import requests
from bs4 import BeautifulSoup
import os

# Target: MyDealz search for 'Sunday Natural'
URL = "https://www.mydealz.de/search?q=sunday%20natural"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def check_for_deals():
    response = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Logic: Look for "hot" deals or specific keywords
    deals = soup.find_all('a', class_='cept-tt') # Title class for MyDealz
    found_deals = []
    
    for deal in deals:
        title = deal.get_text().lower()
        if "sunday natural" in title:
            found_deals.append(deal.get_text().strip())
    
    return found_deals

if __name__ == "__main__":
    new_deals = check_for_deals()
    if new_deals:
        print(f"FOUND: {new_deals[0]}")
        # Save to a file to send via GitHub Actions later
        with open("deal_found.txt", "w") as f:
            f.write("\n".join(new_deals))
