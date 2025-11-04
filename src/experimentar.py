from collectors.continente.collector import ContinenteCollector

def test_continente_scraper():
    collector = ContinenteCollector()
    products_html = collector.fetch()
    products = collector.parse(products_html)
    collector.save_products_to_file(products)
    assert isinstance(products, list)
    assert all("name" in p and "unit_price" in p for p in products)
    print("Scraper test passed!")

if __name__ == "__main__":
    test_continente_scraper()
