from typing import Dict
import json
import os

def load_json_file(file_path: str) -> Dict:
    """Load and parse JSON from a local file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_txt_to_file(file_path: str, content: str):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

def save_json_to_file(file_path: str, content):
    """Save content to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=4, ensure_ascii=False)