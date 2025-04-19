import requests
import pandas as pd


def load_transactions(org_id, page, limit, token):
    url = f"http://localhost:8080/api/transactions?organization_id={org_id}&page={page}&limit={limit}"
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return None, f"Ошибка загрузки данных: {e}"

    flattened = []
    for entry in data:
        for product in entry["products"]:
            flattened.append({
                "entry_id": entry["id"],
                "cashboxId": entry["cashboxId"],
                "paymentMethod": entry["paymentMethod"],
                "totalAmount": entry["totalAmount"],
                "organizationId": entry["organizationId"],
                "created_at": entry["created_at"],
                "product_id": product["id"],
                "product_name": product["name"],
                "product_price": product["price"],
                "product_description": product["description"],
                "product_sizes": ', '.join(product["sizes"]) if product["sizes"] else '',
                "product_colors": ', '.join(product["colors"]) if product["colors"] else '',
            })
    return pd.DataFrame(flattened), None
