import requests
from bs4 import BeautifulSoup

# Target: MyDealz search for Sunday Natural
URL = "https://www.mydealz.de/search?q=sunday%20natural"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_for_deals():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all deal title links
        deals = soup.find_all('a', class_='cept-tt')
        found_entries = []
        
        for deal in deals:
            title = deal.get_text().strip()
            # This grabs the actual URL link
            link = deal.get('href')
            
            # Filter for your brand
            if "sunday natural" in title.lower():
                # MyDealz links are often relative (starting with /)
                # We turn them into full clickable links
                if link and link.startswith('/'):
                    link = f"https://www.mydealz.de{link}"
                
                found_entries.append(f"PROMO: {title}\nCLICK HERE: {link}")
        
        return found_entries
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

if __name__ == "__main__":
    results = check_for_deals()
    with open("deal_found.txt", "w") as f:
        if results:
            # This puts a clear line between different deals
            f.write("\n\n====================\n\n".join(results))
        else:
            f.write("") # Leave empty if nothing found
