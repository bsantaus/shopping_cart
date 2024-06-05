from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, select
from config import settings
from main import app
from models import *
import json
import pytest

client = TestClient(app)

def test_add_remove_item_from_cart():
    # Create cart 
    res = client.put("/cart", json={
        "name": "test cart"
    })

    assert res.status_code == 200

    cart = json.loads(res.content)

    # Create items

    res = client.put("/item", json={
        "name": "apple"
    })

    assert res.status_code == 200
    apple = json.loads(res.content)

    res = client.put("/item", json={
        "name": "banana"
    })

    assert res.status_code == 200
    banana = json.loads(res.content)

    # add two apples and one banana
    res = client.put(f"/cart/{cart['id']}/item/{apple['id']}")
    assert res.status_code == 200
    res = client.put(f"/cart/{cart['id']}/item/{apple['id']}")
    assert res.status_code == 200
    res = client.put(f"/cart/{cart['id']}/item/{banana['id']}")
    assert res.status_code == 200


    res = client.get(f"/cart/{cart['id']}")
    assert res.status_code == 200

    cart_summary = json.loads(res.content)
    assert "cart" in cart_summary
    assert cart_summary["cart"]["id"] == cart["id"]
    assert cart_summary["cart"]["name"] == cart["name"]

    assert "items" in cart_summary
    assert len(cart_summary["items"]) == 2
    
    for item in cart_summary["items"]:
        fruit = item["item"]["name"]
        quantity = item["quantity"]

        if fruit == "apple":
            assert quantity == 2
        elif fruit == "banana": 
            assert quantity == 1
        else:
            print("unexpected item present in cart!")
            assert False

    res = client.delete(f"/cart/{cart['id']}/item/{apple['id']}")
    assert res.status_code == 200
    res = client.delete(f"/cart/{cart['id']}/item/{banana['id']}")
    assert res.status_code == 200

    res = client.get(f"/cart/{cart['id']}")
    assert res.status_code == 200

    cart_summary = json.loads(res.content)

    # expect that banana record is deleted
    assert len(cart_summary["items"]) == 1
    
    for item in cart_summary["items"]:
        fruit = item["item"]["name"]
        quantity = item["quantity"]

        if fruit == "apple":
            assert quantity == 1
        else:
            print("unexpected item present in cart!")
            assert False

    # cleanup

    _ = client.delete(f"/cart/{cart['id']}")
    _ = client.delete(f"/item/{apple['id']}")
    _ = client.delete(f"/item/{banana['id']}")


def test_remove_nonexistent_item():
    # Create cart 
    res = client.put("/cart", json={
        "name": "test cart"
    })

    assert res.status_code == 200

    cart = json.loads(res.content)

    # Create item

    res = client.put("/item", json={
        "name": "apple"
    })

    assert res.status_code == 200
    apple = json.loads(res.content)

    # Apple not in cart, but exists in DB.

    # Test that deleting item not in cart throws 404.
    res = client.delete(f"/cart/{cart['id']}/item/{apple['id']}")
    assert res.status_code == 404


