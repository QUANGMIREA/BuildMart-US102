-- US-102: expand products by unit, then backfill known historical SKUs.
-- Do not silently assign the same default unit to unrelated materials.
ALTER TABLE products ADD COLUMN unit TEXT;
UPDATE products SET unit = 'мешок' WHERE sku = 'CEMENT-M500';
UPDATE products SET unit = 'м³' WHERE sku = 'SAND';
-- In a production deployment, validate any unmapped SKUs before approval.
