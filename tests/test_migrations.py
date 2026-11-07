import sqlite3
from scripts.migrate import run_migrations


def test_migration_v001_then_v002_backfills_historical_products(tmp_path):
    db_path = tmp_path / 'catalog.db'
    assert run_migrations(db_path, target='V001') == ['V001']
    with sqlite3.connect(db_path) as conn:
        fields = [row[1] for row in conn.execute('PRAGMA table_info(products)')]
        assert 'unit' not in fields
        assert conn.execute('SELECT count(*) FROM products').fetchone()[0] == 2

    assert run_migrations(db_path) == ['V002']
    with sqlite3.connect(db_path) as conn:
        units = dict(conn.execute('SELECT sku, unit FROM products'))
        assert units == {'CEMENT-M500': 'мешок', 'SAND': 'м³'}
        version_count = conn.execute('SELECT COUNT(*) FROM schema_migrations').fetchone()[0]
        assert version_count == 2
    assert run_migrations(db_path) == []


def test_bad_migration_target_is_rejected(tmp_path):
    import pytest
    with pytest.raises(ValueError):
        run_migrations(tmp_path / 'db.sqlite3', target='V999')
