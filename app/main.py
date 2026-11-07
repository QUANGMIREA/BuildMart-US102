"""Baseline catalog before US-102 is implemented."""
import os
import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException


def create_app(db_path: str | Path | None = None) -> FastAPI:
    path = Path(db_path or os.getenv('BUILDMART_DB_PATH', 'data/buildmart.db'))
    api = FastAPI(title='BuildMart - учебный пример')

    @api.get('/health')
    def health():
        return {'status': 'ok'}

    @api.get('/products')
    def get_products():
        if not path.is_file():
            raise HTTPException(status_code=503, detail='Database is not initialized')
        with sqlite3.connect(path) as conn:
            conn.row_factory = sqlite3.Row
            return [dict(row) for row in conn.execute(
                'SELECT id, sku, name, price_rub FROM products ORDER BY id'
            )]

    return api


app = create_app()
