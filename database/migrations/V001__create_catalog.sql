CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    price_rub INTEGER NOT NULL CHECK (price_rub >= 0)
);

-- DEMO RECORDS: do not import test catalog into a real production store.
INSERT INTO products(id, sku, name, price_rub) VALUES
  (1, 'CEMENT-M500', 'Цемент М500', 450),
  (2, 'SAND', 'Песок', 1200);
