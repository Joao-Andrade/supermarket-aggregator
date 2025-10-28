from abc import ABC, abstractmethod
import json
from typing import List, Dict

class BaseScraper(ABC):
    @abstractmethod
    def fetch(self, query: str) -> str:
        """Fetch raw HTML or JSON"""
        pass

    @abstractmethod
    def parse(self, raw_data: str) -> List[Dict]:
        """Parse HTML/JSON to product list"""
        pass

    def get_products(self, query: str) -> List[Dict]:
        """Run fetch + parse in one call"""
        raw_data = self.fetch(query)
        return self.parse(raw_data)

    def save_to_file(self, products: List[Dict], filename: str = "products.json"):
        """Save the list of products to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(products, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(products)} products to {filename}")