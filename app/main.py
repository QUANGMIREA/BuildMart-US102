"""BuildMart catalog API after US-102, backed by versioned SQLite data."""
import os
import sqlite3
from contextlib import closing
from pathlib import Path
from fastapi import FastAPI, HTTPException
from app.catalog import is_valid_unit


def create_app(db_path: str | Path | None = None) -> FastAPI:
    path = Path(db_path or os.getenv('BUILDMART_DB_PATH', 'data/buildmart.db'))
    api = FastAPI(title='BuildMart - учебный пример')

    @api.get('/health')
    def health():
        return {'status': 'ok'}

    @api.get('/products')
    def get_products(unit: str | None = None):
        if not path.is_file():
            raise HTTPException(status_code=503, detail='Database is not initialized')
        with closing(sqlite3.connect(path)) as conn:
            conn.row_factory = sqlite3.Row
            if unit is None:
                rows = conn.execute(
                    'SELECT id, sku, name, price_rub, unit FROM products ORDER BY id'
                ).fetchall()
            else:
                rows = conn.execute(
                    'SELECT id, sku, name, price_rub, unit FROM products WHERE unit = ? ORDER BY id',
                    (unit,)
                ).fetchall()
        products = [dict(row) for row in rows]
        if any(not is_valid_unit(product['unit']) for product in products):
            raise HTTPException(status_code=500, detail='Invalid product unit in database')
        return products

    @api.get('/products/{product_id}')
    def get_product(product_id: int):
        if not path.is_file():
            raise HTTPException(status_code=503, detail='Database is not initialized')
        with closing(sqlite3.connect(path)) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                'SELECT id, sku, name, price_rub, unit FROM products WHERE id = ?',
                (product_id,)
            ).fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail='Product not found')
        product = dict(row)
        if not is_valid_unit(product['unit']):
            raise HTTPException(status_code=500, detail='Invalid product unit in database')
        return product

    return api


app = create_app()
