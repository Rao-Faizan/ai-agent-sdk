import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        # Website se data lo
        response = requests.get(url)
        response.raise_for_status()  # Error check karo
        
        # HTML parse karo
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Saare paragraphs nikalo
        paragraphs = soup.find_all('p')
        content = [p.get_text().strip() for p in paragraphs]
        
        return "\n".join(content)
    except Exception as e:
        return f"Error scraping website: {e}"

# Test karo
url = "https://ait.iak.ngo/"
website_data = scrape_website(url)
print("Website Content:\n", website_data)






# 