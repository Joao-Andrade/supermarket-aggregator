from typing import List, Dict
import json
import os

def save_products_to_file(products: List[Dict], filename: str = "products.json", append: bool = False):
    """
    Save the list of products to a JSON file.
    Can either overwrite the file or append to it.
    """
    file_content = ""
    if append and os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "r", encoding="utf-8") as f:
            file_content = f.read()

    output_products = products
    if file_content:
        existing_products = json.loads(file_content)
        if isinstance(existing_products, list):
            output_products = existing_products + products

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output_products, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(products)} products to {filename}")

def load_json_file(path):
    """Load and parse JSON from a local file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data