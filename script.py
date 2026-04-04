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
        
        # We look for the main deal "articles" to check status + title
        # In MyDealz, deals are usually wrapped in an <article> or <div>
        # but checking the 'thread' class is the most reliable way to find 'expired' markers.
        threads = soup.find_all('div', class_='thread--deal')
        found_entries = []
        
        for thread in threads:
            # 1. Check if the deal is expired
            # MyDealz adds 'mute--text' or 'is-expired' classes to old deals
            is_expired = thread.find(class_=lambda x: x and ('is-expired' in x or 'mute--text' in x))
            
            # Get the link/title element
            link_tag = thread.find('a', class_='cept-tt')
            if not link_tag:
                continue

            title = link_tag.get_text().strip().lower()
            
            # 2. Filtering Logic: 
            # - Must contain "sunday natural"
            # - Must NOT be expired (no 'Abgelaufen' text or expired class)
            if "sunday natural" in title:
                if is_expired or "abgelaufen" in thread.get_text().lower() or "expired" in thread.get_text().lower():
                    continue  # Skip this deal
                
                link = link_tag.get('href')
                if link and link.startswith('/'):
                    link = f"https://www.mydealz.de{link}"
                
                found_entries.append(f"LIVE PROMO: {link_tag.get_text().strip()}\nCLICK HERE: {link}")
        
        return found_entries
    except Exception as e:
        print(f"Scraping error: {e}")
        return []

if __name__ == "__main__":
    results = check_for_deals()
    with open("deal_found.txt", "w") as f:
        if results:
            f.write("\n\n====================\n\n".join(results))
        else:
            f.write("")
