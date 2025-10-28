from bs4 import BeautifulSoup

# Load HTML
with open("continente.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

products = []

# Each product block
for product in soup.select("div.product[data-pid]"):
    pid = product.get("data-pid")

    # Brand
    brand_tag = product.select_one(".pwc-tile--brand")
    brand = brand_tag.get_text(strip=True) if brand_tag else None

    # Name (description)
    name_tag = product.select_one(".pwc-tile--description")
    name = name_tag.get_text(strip=True) if name_tag else None

    # Price
    price_tag = product.select_one(".price .value, .sales .value")
    price = price_tag.get_text(strip=True).replace("\xa0", " ") if price_tag else None

    if name or brand or price:
        products.append({
            "pid": pid,
            "brand": brand,
            "name": name,
            "price": price
        })

# Print results
for p in products:
    print(f"{p['pid']} | {p['brand']} | {p['name']} | {p['price']}")
