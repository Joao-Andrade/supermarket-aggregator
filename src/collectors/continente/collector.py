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

    def fetch(self, query: str = None) -> str:
        """
        Fetches the raw HTML for a given search query.
        The base URL is for searching, so we'll use a query parameter.
        """
        if not query:
            query = ""
        return http_utils.get_page(self.base_url + f"pesquisa/?q={query}")
    
    def fetch_all_categories(self) -> List[Dict]:
        """Fetch and parse products from all categories defined in categories.json."""
        all_products = []
        
        # Construct the path to categories.json relative to the current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        categories_path = os.path.join(current_dir, 'categories.json')

        with open(categories_path, 'r') as f:
            categories = json.load(f)

        for category_path in categories:
            category_url = self.base_url + category_path
            raw_data = http_utils.get_page(category_url)
            all_products.extend(self.parse(raw_data))
        return all_products

    def parse(self, raw_data: str) -> List[Dict]:
        """
        Parses the HTML content to extract product details.
        """
        soup = BeautifulSoup(raw_data, 'html.parser')
        products = []

        # Find the "Show More" button to get the URL for the next page
        show_more_container = soup.select_one(".infinite-scroll-placeholder")
        if show_more_container and show_more_container.has_attr('data-url'):
            next_page_url = show_more_container['data-url']
            print(f"Found 'Show More' button. Next page URL: {next_page_url}")
            # Ready to fetch this URL to get more products.

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
