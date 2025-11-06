from abc import ABC, abstractmethod
from typing import List, Dict
from .utils import file as file_utils

class BaseCollector(ABC):

    def __init__(self, store_name: str, base_url: str):
        self.store_name = store_name
        self.base_url = base_url

    @abstractmethod
    def fetch_all_categories(self, combine_categories: bool = False) -> List[Dict]:
        """Fetch raw HTML or JSON from every category
        Example:
        [
            {"category1": ["<html></html>"]}
        ]
        If combine_categories:
        [
        "<html></html>"
        ]
        """
        pass

    @abstractmethod
    def fetch_specific_category(self, category_index: int = 0) -> List[str]:
        """Fetch raw HTML or JSON from a specific category index from categories.json
        Example:
        [
            "<html></html>"
        ]
        """
        pass

    @abstractmethod
    def fetch(self, query: str = "", endpoint: str = "pesquisa?q=") -> List[str]:
        """Fetch raw HTML or JSON
        Example:
        [
            "<html></html>"
        ]
        """
        pass

    @abstractmethod
    def parse(self, raw_data: List[str]) -> List[Dict]:
        """Parse HTML/JSON to product list"""
        pass

    def save_products_to_file(self, products: List[Dict], filename: str = "products.json", append: bool = False):
        """Save the list of products to a JSON file."""
        file_utils.save_products_to_file(products, filename, append=append)