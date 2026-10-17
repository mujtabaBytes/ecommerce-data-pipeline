import json
from pathlib import Path
from datetime import datetime, timezone

import requests

URL = "https://dummyjson.com/products?limit=100"


def extract_products():
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    payload = response.json()
    products = payload["products"]

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%SZ"
    )
    output_file = output_dir / f"products_{timestamp}.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2)

    print(f"API status: {response.status_code}")
    print(f"Products extracted: {len(products)}")
    print(f"Total products reported by API: {payload['total']}")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    extract_products()
