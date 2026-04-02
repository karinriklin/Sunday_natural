import requests
from bs4 import BeautifulSoup

# The keywords you care about
AMINO_KEYWORDS = ["amino", "bcaa", "eaa", "protein", "aminosäuren", "komplex"]

# Target sites
TARGETS = [
    {"name": "Influencer Codes", "url": "https://sunday.couponasion.com/"},
    {"name": "Official Sale Page", "url": "https://www.sunday.de/sale.html"}
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_for_aminos():
    findings = []
    
    for target in TARGETS:
        try:
            response = requests.get(target["url"], headers=HEADERS, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Search for Text/Sale mentions
            # We look for any text that mentions "Amino" or similar
            text_elements = soup.find_all(string=lambda t: any(k in t.lower() for k in AMINO_KEYWORDS))
            
            for element in text_elements:
                clean_text = element.strip()
                if 10 < len(clean_text) < 100: # Filter for readable phrases
                    findings.append(f"[{target['name']}] Found: {clean_text}")

            # 2. Specifically look for Codes on the aggregator site
            if "couponasion" in target["url"]:
                # These codes were recently seen working (April 2026)
                # We extract them if they are near 'Sunday' or 'Amino' keywords
                codes = soup.find_all(['code', 'span'], class_=lambda x: x and 'code' in x.lower())
                for c in codes:
                    code_val = c.get_text().strip()
                    if 3 < len(code_val) < 12:
                        findings.append(f"Potential Influencer Code: {code_val}")

        except Exception as e:
            print(f"Error on {target['name']}: {e}")
            
    return list(set(findings)) # Remove duplicates

if __name__ == "__main__":
    results = check_for_aminos()
    with open("deal_found.txt", "w") as f:
        if results:
            f.write("SUNDAY NATURAL AMINO ACID ALERTS:\n\n")
            f.write("\n".join(results))
            f.write("\n\nCheck official sets here: https://www.sunday.de/en/amino-acid-mix/")
        else:
            f.write("")
