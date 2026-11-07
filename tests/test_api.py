from fastapi.testclient import TestClient
from app.main import create_app


def test_health(migrated_db):
    client = TestClient(create_app(migrated_db))
    assert client.get('/health').json() == {'status': 'ok'}


def test_products(migrated_db):
    client = TestClient(create_app(migrated_db))
    response = client.get('/products')
    assert response.status_code == 200
    assert len(response.json()) == 2
