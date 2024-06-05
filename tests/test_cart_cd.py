from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, select
from config import settings
from main import app
from models import *
import json
import pytest

client = TestClient(app)

@pytest.fixture
def db():
    conn_str = (
        "postgresql://{user}:{password}@{host}:{port}/{database}"
        .format(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB
        )
    )
    return create_engine(conn_str)

def get_all_carts(db):
    with Session(db) as session:
        stmt = select(Cart)
        carts = session.exec(stmt)
        all_carts = list(carts.all())
    return all_carts

# def test_check():
#     res = client.get("/check")
#     assert res.status_code == 200
#     healthcheck = json.loads(str(res.content, "utf-8"))

#     assert healthcheck["message"] == "Server Ready"
#     assert healthcheck["database_status"] == "Connected"
#     assert "timestamp" in healthcheck

def test_create_and_delete_carts(db):
    res = client.put("/cart", json={
        "name": "Create Test 0"
    })
    assert res.status_code == 200
    cart_0 = json.loads(res.content)
    assert "id" in cart_0 and type(cart_0["id"]) == int
    assert "name" in cart_0 and cart_0["name"] == "Create Test 0"

    carts = get_all_carts(db)

    assert len(carts) >= 1
    cart = carts[0]
    print(cart)
    assert cart.name == "Create Test 0"

    res = client.put("/cart", json={
        "name": "Create Test 1"
    })
    assert res.status_code == 200
    cart_1 = json.loads(res.content)
    assert "id" in cart_1 and type(cart_1["id"]) == int
    assert "name" in cart_1 and cart_1["name"] == "Create Test 1"

    carts = get_all_carts(db)
    assert len(carts) >= 2
    
    prev_carts_len = 2
    for cart in carts:
        res = client.delete(f"/cart/{cart.id}")
        assert res.status_code == 200

        fewer_carts = get_all_carts(db)
        assert len(fewer_carts) < prev_carts_len
        prev_carts_len -= 1
        assert cart.id not in [c.id for c in fewer_carts]
        

def test_delete_nonexistent_cart():
    res = client.delete("/cart/1000")
    assert res.status_code == 404
    message = json.loads(res.content)["message"]

    assert message == "Cart with ID 1000 does not exist"

    res = client.put("/cart", json={
        "name": "Create Test 0"
    })
    new_id = json.loads(res.content)["id"]
    res = client.delete(f"/cart/{new_id}")
    assert res.status_code == 200
    
    res = client.delete(f"/cart/{new_id}")
    assert res.status_code == 404



