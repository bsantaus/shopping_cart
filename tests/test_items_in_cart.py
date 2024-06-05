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

def get_all_items(db):
    with Session(db) as session:
        stmt = select(Item)
        items = session.exec(stmt)
        all_items = list(items.all())
    return all_items

def test_add_remove_item_from_cart(db):
    pass