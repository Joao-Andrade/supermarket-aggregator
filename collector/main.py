from collectors.europe.pt.continente.collector import ContinenteCollector

def test_continente_collector():
    collector = ContinenteCollector()
    collector.search_category(0)


if __name__ == "__main__":
    test_continente_collector()