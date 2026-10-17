import json
from pathlib import Path

import psycopg


def load_products():
    raw_files = sorted(Path("data/raw").glob("products_*.json"))

    if not raw_files:
        raise FileNotFoundError(
            "No JSON files found. Run src/extract.py first."
        )

    with raw_files[-1].open(encoding="utf-8") as file:
        payload = json.load(file)

    products = payload["products"]

    rows = [
        (
            p["id"],
            p["title"],
            p.get("category"),
            p.get("price"),
            p.get("rating"),
            p.get("stock"),
        )
        for p in products
    ]

    with psycopg.connect("dbname=ecommerce_dw") as conn:
        with conn.cursor() as cur:
            cur.executemany(
                """
                INSERT INTO products
                    (product_id, title, category, price, rating, stock)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (product_id) DO UPDATE SET
                    title = EXCLUDED.title,
                    category = EXCLUDED.category,
                    price = EXCLUDED.price,
                    rating = EXCLUDED.rating,
                    stock = EXCLUDED.stock,
                    loaded_at = CURRENT_TIMESTAMP
                """,
                rows,
            )

    print(f"Products processed: {len(rows)}")
    print("Data loaded successfully into PostgreSQL.")


if __name__ == "__main__":
    load_products()
