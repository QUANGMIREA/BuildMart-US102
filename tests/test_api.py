from fastapi.testclient import TestClient
from app.main import create_app


def test_health(migrated_db):
    client = TestClient(create_app(migrated_db))
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_list_products_contains_unit(migrated_db):
    client = TestClient(create_app(migrated_db))
    response = client.get('/products')
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == 2
    assert all(row['unit'] for row in rows)
    assert rows[0]['unit'] == 'мешок'
    assert rows[1]['unit'] == 'м³'


def test_filter_cement_unit(migrated_db):
    client = TestClient(create_app(migrated_db))
    response = client.get('/products', params={'unit': 'мешок'})
    assert response.status_code == 200
    assert [product['sku'] for product in response.json()] == ['CEMENT-M500']


def test_filter_unknown_unit(migrated_db):
    client = TestClient(create_app(migrated_db))
    response = client.get('/products', params={'unit': 'khong-ton-tai'})
    assert response.status_code == 200
    assert response.json() == []


def test_get_product(migrated_db):
    client = TestClient(create_app(migrated_db))
    response = client.get('/products/2')
    assert response.status_code == 200
    assert response.json()['unit'] == 'м³'


def test_missing_product(migrated_db):
    client = TestClient(create_app(migrated_db))
    response = client.get('/products/999')
    assert response.status_code == 404


def test_missing_database(tmp_path):
    client = TestClient(create_app(tmp_path / 'missing.db'))
    response = client.get('/products')
    assert response.status_code == 503
    assert client.get('/products/1').status_code == 503


def test_invalid_stored_unit_is_detected(migrated_db):
    import sqlite3
    from contextlib import closing

    with closing(sqlite3.connect(migrated_db)) as conn:
        conn.execute(
            "INSERT INTO products(id, sku, name, price_rub, unit) VALUES(3, 'INVALID', 'Bad', 2, 'liter')"
        )
        conn.commit()
    client = TestClient(create_app(migrated_db))
    assert client.get('/products').status_code == 500
    assert client.get('/products/3').status_code == 500
