import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from .base_scraper import BaseScraper
class ContinenteScraper(BaseScraper):
    store_name = "Continente"
    # q=iogurte&pmin=0%2e01&srule=price-low-to-high&start=72&sz=36
    base_url = "https://www.continente.pt/pesquisa/?start=0&sz=4&q="

    def fetch(self, query: str) -> str:
        """Fetch the HTML content for a given search query."""
        url = f"{self.base_url}{query}"
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    def parse(self, raw_data: str) -> List[Dict]:
        """Parse the HTML content to extract product details."""
        soup = BeautifulSoup(raw_data, 'html.parser')
        self.save_html_to_file(soup)
        a = soup.find("div", class_="row search-results-wrap")
        print(a.get("data-gtm-results"))
        products = []

        # Find all product containers
        product_containers = soup.find_all('div', class_='product-card')

        for container in product_containers:
            name_tag = container.find('span', class_='product-card-title')
            price_tag = container.find('span', class_='product-card-price')

            if name_tag and price_tag:
                name = name_tag.get_text(strip=True)
                price = price_tag.get_text(strip=True).replace('€', '').replace(',', '.')

                # Handle missing or malformed price data
                try:
                    price = float(price)
                except ValueError:
                    continue  # Skip this product if price is invalid

                products.append({
                    'store': self.store_name,
                    'name': name,
                    'price': price,
                    'url': container.find('a')['href']
                })

        return products


    def save_html_to_file(self, html_content: str, filename: str = "continente.html"):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_content.prettify())