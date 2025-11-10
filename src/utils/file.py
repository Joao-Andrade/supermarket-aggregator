from typing import Dict
import json
import os

def load_json_file(file_path: str) -> Dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, file_path)
    """Load and parse JSON from a local file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data