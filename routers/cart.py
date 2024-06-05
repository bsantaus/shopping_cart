from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from models import Cart, Item, CartSummary, Error
from typing import Union, Optional

from services import sc_database

cart_router = APIRouter()

@cart_router.put('/cart', response_model=Cart, responses={'500': {'model': Error}})
def put_cart(cart: Cart = None) -> Union[Cart, Error]:
    """
    Create New Shopping Cart
    """
    
    ok, db_cart = sc_database().create(cart)
    
    if ok:
        return db_cart
    else:
        return JSONResponse(
            status_code=500,
            content=dict(
                Error(
                    message="Error while creating cart",
                )
            )
        )


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
    
    ok, num_deleted = sc_database().delete(Cart, id=cart_id)
    
    if ok:
        if num_deleted == 1:
            return "Deleted"
        elif num_deleted == 0:
            return JSONResponse(
            status_code=404,
            content=dict(
                Error(
                    message=f"Cart with ID {cart_id} does not exist",
                )
            )
        )
    
    return JSONResponse(
        status_code=500,
        content=dict(
            Error(
                message="Error while deleting cart"
            )
        )
    )


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