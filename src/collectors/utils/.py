import requests

def get_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text