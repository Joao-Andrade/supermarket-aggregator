from collectors.base_collector import BaseCollector
import os
from bs4 import BeautifulSoup
import re
import hashlib
from datetime import datetime, timezone

class ContinenteCollector(BaseCollector):

    def __init__(self, name: str = "Continente", base_url: str = "https://www.continente.pt/", country_code: str = "pt"):
        """
        Initializes the ContinenteCollector with the store name, base URL and country code.
        """
        self.collector_path = os.path.dirname(__file__)
        super().__init__(name, base_url, country_code)

    def get_categories(self) -> dict:
        return self.load_json(f"{self.collector_path}/categories.json")

    def search_category(self, category: int = 0, for_range: int = 30):
        products = []
        categories_file = self.get_categories()
        page = self.get_page(f"{self.base_url}/{categories_file[category]}&start=0&sz={for_range}")
        page_products = self.parse_page(page)
        self.output_products(page_products, "file", f"{self.collector_path}/../../../../example_files/continente0.json")
        products.extend(page_products)
        n_products = self.get_total_products(page)
        for i in range(for_range, n_products+for_range, for_range):
            page = self.get_page(f"{self.base_url}/{categories_file[category]}&start={i}&sz={for_range}")
            print(f"{self.base_url}/{categories_file[category]}&start={i}&sz={for_range}")
            page_products = self.parse_page(page)
            self.output_products(page_products, "file", f"{self.collector_path}/../../../../example_files/continente{i}.json")
            products.extend(page_products)
        return products
            
    def get_total_products(self, page: str) -> int:
        """
        Parses the HTML to find the total number of products.
        """
        soup = BeautifulSoup(page, 'html.parser')
        grid_footer = soup.find("div", class_="grid-footer")
        if grid_footer and grid_footer.has_attr('data-total-count'):
            return int(grid_footer['data-total-count'])
        return 0
    
    def parse_page(self, page: str) -> list[dict]:
        products = []
        now = datetime.now(timezone.utc)
        last_fetch_iso = now.strftime("%Y-%m-%dH%H:%M")
        last_fetch_epoch = int(now.timestamp())

        soup = BeautifulSoup(page, 'html.parser')
        for product_tile in soup.select(".product-tile"):
            # Extract the product name
            name = product_tile.select_one(".pwc-tile--description")
            name_text = name.text.strip() if name else "no-name-error"
            normalized_name = re.sub(r'[^a-z0-9-\s]', '', name_text.lower()).replace(' ', '-')

            # Extract the brand
            brand = product_tile.select_one(".pwc-tile--brand")
            brand_text = brand.text.strip() if brand else self.store_name
            normalized_brand = re.sub(r'[^a-z0-9-\s]', '', brand_text.lower()).replace(' ', '-')

            # Extract unit and kg prices
            price_element = product_tile.select_one(".pwc-tile--price-primary .ct-price-formatted")
            bulk_price_element = product_tile.select_one(".pwc-tile--price-secondary")
            price_text = float(price_element.text.strip()[1:].replace(',','.')) if price_element else -1
            bulk_price = bulk_price_element.text.strip().split('/') if bulk_price_element else ["$-1.0", "kg"]
            bulk_price_text = float(bulk_price[0][1:].strip().replace(',','', bulk_price[0].count(',')-1).replace(',','.'))
            price_unit = bulk_price[1].strip() if bulk_price else ''

            # Extract product and image URLs
            product_link = product_tile.select_one(".ct-image-container a")
            product_url = product_link['href'] if product_link else None
            image = product_tile.select_one(".ct-image-container img")
            image_url = image['data-src'] if image and 'data-src' in image.attrs else (image['src'] if image and 'src' in image.attrs else None)
            products.append({
                "name": name_text,
                "normalized_name": normalized_name,
                "brand": brand_text,
                "normalized_brand": normalized_brand,
                "url": product_url,
                "image_url": image_url,
                "country_code": self.country_code,
                "store_name": self.store_name,
                "unit_price": price_text,
                "bulk_price": bulk_price_text,
                "price_unit": price_unit,
                "last_fetch_iso": last_fetch_iso,
                "last_fetch_epoch": last_fetch_epoch
            })

        return products
    
