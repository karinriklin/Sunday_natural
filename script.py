import requests
from bs4 import BeautifulSoup

# Define multiple targets
TARGETS = [
    {"name": "Coupon Site", "url": "https://sunday.couponasion.com/"},
    {"name": "Official Sale", "url": "https://www.sunday.de/sale.html"}
]

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_site(target):
    try:
        response = requests.get(target["url"], headers=HEADERS, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        findings = []

        if "couponasion" in target["url"]:
            # Looks for things that look like actual codes (usually in bold or spans)
            codes = soup.find_all(['code', 'span', 'div'], class_=lambda x: x and 'code' in x.lower())
            for c in codes:
                code_text = c.get_text().strip()
                if 3 < len(code_text) < 15: # Filter out noise
                    findings.append(f"Potential Code: {code_text}")
        
        elif "sunday.de" in target["url"]:
            # Look for percentage discounts on the official page
            sales = soup.find_all(string=lambda text: "%" in text)
            for s in sales:
                if len(s.strip()) < 50: # Avoid long paragraphs
                    findings.append(f"Official Sale: {s.strip()}")

        return findings
    except:
        return []

if __name__ == "__main__":
    all_results = []
    for t in TARGETS:
        res = scrape_site(t)
        if res:
            all_results.append(f"--- {t['name']} ---")
            all_results.extend(res)

    with open("deal_found.txt", "w") as f:
        f.write("\n".join(all_results))
