import psycopg


def run_transformations():
    with psycopg.connect("dbname=ecommerce_dw") as conn:
        with conn.cursor() as cur:

            print("\n--- Product count ---")
            cur.execute("SELECT COUNT(*) FROM products")
            print(cur.fetchone()[0])

            print("\n--- Average price by category ---")
            cur.execute("""
                SELECT
                    category,
                    COUNT(*) AS product_count,
                    ROUND(AVG(price), 2) AS average_price
                FROM products
                GROUP BY category
                ORDER BY average_price DESC NULLS LAST
            """)

            for row in cur.fetchall():
                print(row)

            print("\n--- Low-stock products (stock < 10) ---")
            cur.execute("""
                SELECT product_id, title, stock
                FROM products
                WHERE stock < 10
                ORDER BY stock ASC
                LIMIT 20
            """)

            for row in cur.fetchall():
                print(row)

            print("\n--- Data-quality issues ---")
            cur.execute("""
                SELECT COUNT(*)
                FROM products
                WHERE title IS NULL
                   OR price < 0
                   OR rating < 0
                   OR rating > 5
                   OR stock < 0
            """)

            print("Invalid records:", cur.fetchone()[0])


if __name__ == "__main__":
    run_transformations()
