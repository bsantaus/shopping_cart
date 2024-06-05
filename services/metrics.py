from typing import Callable
from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_client import Gauge

from services import sc_database
from models import *

def mean_cart_size() -> Callable[[Info], None]:
    METRIC = Gauge(
        'mean_cart_size',
        'Average cart size at reading'
    )

    def instrumentation(info: Info) -> None:
        METRIC.set(0)
        ok, carts = sc_database().enumerate(Cart)
        if not ok:
            return
        counter = 0
        total_items = 0.
        for cart in carts:
            counter += 1
            ok, items_in_cart = sc_database().retrieve_cart_items(ItemsInCart, cart.id)
            if not ok:
                return
            for item in items_in_cart:
                total_items += item.quantity
        
            METRIC.set(total_items / counter)

    return instrumentation

def total_item_counts() -> Callable[[Info], None]:
    METRIC = Gauge(
        'total_item_counts',
        'Total item counts across carts at reading',
        labelnames=("item_name_ids",)
    )

    def instrumentation(info: Info) -> None:
        ok, items = sc_database().enumerate(Item)
        if not ok:
            return
        item_name_ids = set()
        for item in items:
            name_id = f"{item.name}_{item.id}"
            item_name_ids.add(name_id)
            METRIC.labels(name_id).set(0)
            ok, items_in_cart = sc_database().retrieve_cart_items(ItemsInCart, item.id)
            if not ok:
                return
            for qty in items_in_cart:
                METRIC.labels(name_id).inc(qty.quantity)
        

    return instrumentation


custom_metrics = [
    mean_cart_size,
    total_item_counts
]