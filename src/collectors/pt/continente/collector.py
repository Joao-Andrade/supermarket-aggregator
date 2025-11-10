import json
import os
import re
from typing import List, Dict
import hashlib
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from collectors.base_collector import BaseCollector # This is already correct
from utils import http as http_utils
from utils import file as file_utils

class ContinenteCollector(BaseCollector):

    def __init__(self, name: str = "Continente", base_url: str = "https://www.continente.pt/"):
        """
        Initializes the ContinenteCollector with the store name and base URL.
        """
        super().__init__(name, base_url)
        self.country_code = "pt"

    def get_categories(self, categories_file: str = 'categories.json') -> List[str]:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        categories_path = os.path.join(current_dir, 'categories.json')
        categories = file_utils.load_json_file(categories_path)
        return categories

    def fetch_all_categories(self, combine_categories: bool = False, categories_file: str = 'categories.json') -> List[Dict]:
        """Fetch and parse products from all categories defined in categories.json."""
        response = []
        
        # Construct the path to categories.json relative to the current file
        categories = self.get_categories(categories_file=categories_file)
        
        for category_path in categories:
            category_name = category_path.split("/")[0]
            print(f"Fetching for {category_name}.")
            pages = self.fetch(endpoint = category_path)
            if combine_categories:
                response.extend(pages)
            else:
                response.append({category_name: pages})
        return response
    
    def fetch_specific_category(self, category_index: int = 0, categories_file: str = 'categories.json') -> List[str]:
        """Fetch raw HTML or JSON from a specific category index from categories.json"""
        # Construct the path to categories.json relative to the current file
        categories = self.get_categories(categories_file=categories_file)
        category_path = categories[category_index]
        category_name = category_path.split("/")[0]
        print(f"Fetching for {category_name}.")
        pages = self.fetch(endpoint = category_path)
        return pages
        
    def fetch(self, query: str = "", endpoint: str = "pesquisa?q=") -> List[str]:
        """
        Fetches the raw HTML for a given search query, handling pagination.
        """
        pages = []
        next_page_url = f"{self.base_url}{endpoint}{query}"
        
        while next_page_url:
            current_url = next_page_url
            print(f"Fetching {current_url}")
            page_content = http_utils.get_page(current_url)
            pages.append(page_content)
            soup = BeautifulSoup(page_content, 'html.parser')
            show_more_container = soup.select_one(".infinite-scroll-placeholder")
            if show_more_container and show_more_container.has_attr('data-url'):
                next_page_url = show_more_container['data-url']
            else:
                next_page_url = None
        return pages

    def parse(self, raw_data: List[str]) -> List[Dict]:
        """
        Parses the HTML content to extract product details.
        Falta o pid.
        """
        products = []
        now = datetime.now(timezone.utc)
        last_fetch_iso = now.strftime("%Y-%m-%dH%H:%M")
        last_fetch_epoch = int(now.timestamp())

        for page in raw_data:
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

                uid_string = f"{normalized_brand}-{normalized_name}"
                uid = hashlib.sha256(uid_string.encode('utf-8')).hexdigest()

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
                products.append({"uid": uid,
                                 "name": name_text,
                                 "normalized_name": normalized_name,
                                 "brand": brand_text,
                                 "normalized_brand": normalized_brand,
                                 "price": {
                                     "url": product_url,
                                     "image_url": image_url,
                                     "country_code": self.country_code,
                                     "store_name": self.store_name,
                                     "unit_price": price_text,
                                     "bulk_price": bulk_price_text,
                                     "price_unit": price_unit,
                                     "last_fetch_iso": last_fetch_iso,
                                     "last_fetch_epoch": last_fetch_epoch
                                 }})

        return products
