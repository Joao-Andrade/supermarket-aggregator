import json
import os
from typing import List, Dict
from bs4 import BeautifulSoup
from ..base_collector import BaseCollector
from ..utils import http as http_utils
from ..utils import file as file_utils

class ContinenteCollector(BaseCollector):

    def __init__(self, name: str = "Continente", base_url: str = "https://www.continente.pt/"):
        """
        Initializes the ContinenteCollector with the store name and base URL.
        """
        super().__init__(name, base_url)

    def fetch_all_categories(self, combine_categories: bool = False) -> List[Dict]:
        """Fetch and parse products from all categories defined in categories.json."""
        response = []
        
        # Construct the path to categories.json relative to the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        categories_path = os.path.join(current_dir, 'categories.json')
        categories = file_utils.load_json_file(categories_path)
        
        for category_path in categories:
            category_name = category_path.split("/")[0]
            print(f"Fetching for {category_name}.")
            pages = self.fetch(endpoint = category_path)
            if combine_categories:
                response.extend(pages)
            else:
                response.append({category_name: pages})
            return response
        return response
    
    def fetch_specific_category(self, category_index: int = 0) -> List[str]:
        """Fetch raw HTML or JSON from a specific category index from categories.json"""
        # Construct the path to categories.json relative to the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        categories_path = os.path.join(current_dir, 'categories.json')

        with open(categories_path, 'r') as f:
            categories_on_file = json.load(f)
        return ""
    
    def fetch(self, query: str = "", endpoint: str = "pesquisa?q=") -> List[str]:
        """
        Fetches the raw HTML for a given search query, handling pagination.
        """
        pages = []
        next_page_url = f"{self.base_url}{endpoint}{query}"
        a = 0
        
        while next_page_url:
            current_url = next_page_url
            print(f"Fetching {current_url}")
            page_content = http_utils.get_page(current_url)
            pages.append(page_content[:4])
            soup = BeautifulSoup(page_content, 'html.parser')
            show_more_container = soup.select_one(".infinite-scroll-placeholder")
            if show_more_container and show_more_container.has_attr('data-url'):
                next_page_url = None if a > 2 else show_more_container['data-url']
                a += 1
            else:
                next_page_url = None
        return pages


    def parse(self, raw_data: List[str]) -> List[Dict]:
        """
        Parses the HTML content to extract product details.
        """
        products = []
        for page in raw_data:
            soup = BeautifulSoup(page, 'html.parser')
            for product_tile in soup.select(".product-tile"):
                # Extract the product name
                name = product_tile.select_one(".pwc-tile--description")
                name_text = name.text.strip() if name else None

                # Extract the brand
                brand = product_tile.select_one(".pwc-tile--brand")
                brand_text = brand.text.strip() if brand else None

                # Extract unit and kg prices
                price = product_tile.select_one(".pwc-tile--price-primary .ct-price-formatted")
                bulk_price = product_tile.select_one(".pwc-tile--price-secondary")
                price_text = price.text.strip() if price else None
                bulk_price_text = ' '.join(bulk_price.text.split()) if bulk_price else None

                # Extract product and image URLs
                product_link = product_tile.select_one(".ct-image-container a")
                product_url = product_link['href'] if product_link else None
                image = product_tile.select_one(".ct-image-container img")
                image_url = image['data-src'] if image and 'data-src' in image.attrs else (image['src'] if image and 'src' in image.attrs else None)
                products.append({"name": name_text, "brand": brand_text, "unit_price": price_text, "kg_price": bulk_price_text, "url": product_url, "image_url": image_url})

        return products
