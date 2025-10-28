from scrapers.continente_scraper import ContinenteScraper

def test_continente_scraper():
    scraper = ContinenteScraper()
    products = scraper.get_products("iogurte")
    scraper.save_to_file(products)
    assert isinstance(products, list)
    assert all("name" in p and "price" in p for p in products)
    print("Scraper test passed!")

if __name__ == "__main__":
    test_continente_scraper()
