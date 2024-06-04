from fastapi import APIRouter, Path
from models import Cart, Item, CartSummary, Error
from typing import Union, Optional

cart_router = APIRouter()

@cart_router.put('/cart', response_model=Cart, responses={'500': {'model': Error}})
def put_cart(body: Cart = None) -> Union[Cart, Error]:
    """
    Create New Shopping Cart
    """
    pass


@cart_router.get(
    '/cart/{cartId}',
    response_model=CartSummary,
    responses={'404': {'model': Error}, '500': {'model': Error}},
)
def get_cart_cart_id(
    cart_id: int = Path(..., alias='cartId')
) -> Union[CartSummary, Error]:
    """
    Retrieve items in Cart by ID
    """
    pass


@cart_router.delete(
    '/cart/{cartId}',
    response_model=None,
    responses={'404': {'model': Error}, '500': {'model': Error}},
)
def delete_cart_cart_id(cart_id: int = Path(..., alias='cartId')) -> Optional[Error]:
    """
    Delete Cart by ID
    """
    pass


@cart_router.put('/cart/{cartId}/add/{itemId}', response_model=None)
def put_cart_cart_id_add_item_id(
    cart_id: int = Path(..., alias='cartId'), item_id: int = Path(..., alias='itemId')
) -> None:
    """
    Add Item with ItemID to Cart with CartID
    """
    pass


@cart_router.delete('/cart/{cartId}/add/{itemId}', response_model=None)
def delete_cart_cart_id_add_item_id(
    cart_id: int = Path(..., alias='cartId'), item_id: int = Path(..., alias='itemId')
) -> None:
    """
    Remove Item with ItemID from Cart with CartID
    """
    pass