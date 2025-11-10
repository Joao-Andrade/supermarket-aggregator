from collectors.pt.continente.collector import ContinenteCollector

def test_continente_scraper():
    collector = ContinenteCollector()
    products_html = collector.fetch_specific_category(category_index=0)
    products = collector.parse(products_html)
    collector.save_products_to_file(products)

if __name__ == "__main__":
    test_continente_scraper()
