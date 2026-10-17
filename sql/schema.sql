CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT,
    price NUMERIC(12, 2),
    rating NUMERIC(4, 2),
    stock INTEGER,
    loaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
