from abc import ABC, abstractmethod
from typing import List, Dict
from utils import http as http_utils
from utils import file as file_utils

class BaseCollector(ABC):

    def __init__(self, store_name: str, base_url: str, country_code: str):
        self.store_name = store_name
        self.base_url = base_url
        self.country_code = country_code

    # @abstractmethod
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
    
    def get_page(self, url):
        page = http_utils.get_page(url)
        return page
    
    def load_json(self, path):
        json = file_utils.load_json_file(path)
        return json
    
    def save_txt_file(self, path: str, content: str):
        file_utils.save_txt_to_file(path, content)

    def save_json_file(self, path: str, content: list[dict]):
        file_utils.save_json_to_file(path, content)

    def output_products(self, products: list[dict], output_type: str = "file", destination: str = ""):
        """
        Outputs the collected products to a file or SQS.
        :param products: List of product dictionaries.
        :param output_type: "file" or "sqs".
        :param destination: File path or SQS Queue URL.
        """
        if not products:
            print("No products to output.")
            return

        if output_type == "file":
            if not destination:
                raise ValueError("Destination path is required for file output.")
            self.save_json_file(destination, products)
            print(f"Saved {len(products)} products to {destination}")
            
        elif output_type == "sqs":
            if not destination:
                raise ValueError("Queue URL is required for SQS output.")
            from utils import aws as aws_utils
            aws_utils.send_to_sqs(destination, products)
            print(f"Sent {len(products)} products to SQS: {destination}")
            
        else:
            print(f"Unknown output type: {output_type}")