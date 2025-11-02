import requests
import pandas as pd
import math

# Configuração
CATEGORIA = "frescos"
BASE_URL = "https://www.continente.pt/on/demandware.store/Sites-continente-Site/default/SearchServices-GetProducts"

# Primeira chamada
params = {
    "cgid": CATEGORIA,
    "start": 0,
    "sz": 36,
    "srule": "FRESH-Generico",
}

r = requests.get(BASE_URL, params=params)
r.raise_for_status()
data = r.json()

# Total de produtos
total = int(data["total"])
page_size = len(data["hits"])
num_pages = math.ceil(total / page_size)

print(f"Total: {total} produtos ({num_pages} páginas)")

def extrair(page_json):
    produtos = []
    for h in page_json["hits"]:
        p = h["product"]
        produtos.append({
            "id": p.get("id"),
            "nome": p.get("productName"),
            "marca": p.get("brand"),
            "preco_unidade": p.get("price", {}).get("sales", {}).get("formatted"),
            "preco_quilo": p.get("price", {}).get("unit", {}).get("formatted"),
            "promocao": ", ".join(p.get("badges", [])) if p.get("badges") else None,
            "url": "https://www.continente.pt" + p.get("link", ""),
            "imagem": (p.get("images", {}).get("default", [{}])[0]).get("url"),
        })
    return produtos

# Recolher todas as páginas
todos = []
for start in range(0, total, page_size):
    params["start"] = start
    r = requests.get(BASE_URL, params=params)
    r.raise_for_status()
    todos += extrair(r.json())

# Exportar para CSV
df = pd.DataFrame(todos)
df.to_csv("frescos_continente.csv", index=False)
print(f"{len(df)} produtos guardados em frescos_continente.csv")
