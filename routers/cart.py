from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from models import Cart, Item, CartSummary, Error, ItemsInCart
from typing import Union, Optional

from services import sc_database

cart_router = APIRouter()

def not_found_response(msg):
        return JSONResponse(
            status_code=404,
            content=dict(
                Error(
                    message=msg
                )
            )
        )

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
    ok, cart = sc_database().retrieve(Cart, cart_id)
    if not ok:
        return not_found_response(f"Cart {cart_id} does not exist!")
    
    ok, cart_items = sc_database().retrieve_cart_items(ItemsInCart, cart_id)

    cart_summary = {
        "cart": dict(cart),
        "items": []
    }

    if ok:
        for itemqty in cart_items:
            ok, item = sc_database().retrieve(Item, itemqty.item_id)
            if not ok:
                return not_found_response(f"Cart {cart_id} does not exist!")
        
            cart_summary["items"].append({
                "item": dict(item),
                "quantity": itemqty.quantity
            })

        return CartSummary(**cart_summary)
    
    return JSONResponse(
        status_code=500,
        content=dict(
            Error(
                message="Error while retrieving items in cart"
            )
        )
    )



@cart_router.delete(
    '/cart/{cartId}',
    response_model=None,
    responses={'404': {'model': Error}, '500': {'model': Error}},
)
def delete_cart_cart_id(cart_id: int = Path(..., alias='cartId')) -> Optional[Error]:
    """
    Delete Cart by ID
    """
    
    ok, cart = sc_database().retrieve(Cart, cart_id)
    if not ok:
        if cart == None:
            return not_found_response(f"Cart with ID {cart_id} does not exist")
        else:
            return JSONResponse(
                status_code=500,
                content=dict(
                    Error(
                        message="Error while deleting cart"
                    )
                )
            )
        
    sc_database().clear_cart(ItemsInCart, cart_id)
    ok, num_deleted = sc_database().delete(Cart, id=cart_id)
    
    if ok:
        if num_deleted == 1:
            return "Deleted"
        
    return JSONResponse(
        status_code=500,
        content=dict(
            Error(
                message="Error while deleting cart"
            )
        )
    )


@cart_router.put('/cart/{cartId}/item/{itemId}', response_model=None)
def put_cart_cart_id_add_item_id(
    cart_id: int = Path(..., alias='cartId'), item_id: int = Path(..., alias='itemId')
) -> None:
    """
    Add Item with ItemID to Cart with CartID
    """

    ok, _ = sc_database().retrieve(Cart, cart_id)
    if not ok:
        return not_found_response(f"Cart {cart_id} does not exist!")
    ok, _ = sc_database().retrieve(Item, item_id)
    if not ok:
        return not_found_response(f"Cart {cart_id} does not exist!")


    ok, item_in_cart = sc_database().retrieve_link(ItemsInCart, cart_id, item_id)

    
    if ok:
        if item_in_cart != None:
            item_in_cart.quantity += 1
            ok, _ = sc_database().update(ItemsInCart, item_in_cart.id, item_in_cart)
            if ok:
                return "Added"
        else:
            item_in_cart = ItemsInCart(
                quantity=1,
                cart_id=cart_id,
                item_id=item_id
            )
            ok, _ = sc_database().create(item_in_cart)
            if ok:
                return "Added"

    return JSONResponse(
        status_code=500,
        content=dict(
            Error(
                message="Error while adding item to cart!",
            )
        )
    )

@cart_router.delete('/cart/{cartId}/item/{itemId}', response_model=None)
def delete_cart_cart_id_add_item_id(
    cart_id: int = Path(..., alias='cartId'), item_id: int = Path(..., alias='itemId')
) -> None:
    """
    Remove Item with ItemID from Cart with CartID
    """
    def not_found_response(msg):
        return JSONResponse(
            status_code=404,
            content=dict(
                Error(
                    message=msg
                )
            )
        )

    ok, _ = sc_database().retrieve(Cart, cart_id)
    if not ok:
        return not_found_response(f"Cart {cart_id} does not exist!")
    ok, _ = sc_database().retrieve(Item, item_id)
    if not ok:
        return not_found_response(f"Cart {cart_id} does not exist!")


    ok, item_in_cart = sc_database().retrieve_link(ItemsInCart, cart_id, item_id)

    
    if ok:
        if item_in_cart == None:
            return not_found_response(f"Cart {cart_id} does not contain any of Item {item_id}!")
        else:
            if item_in_cart.quantity <= 1:
                ok, _ = sc_database().delete(ItemsInCart, item_in_cart.id)
            else:
                item_in_cart.quantity -= 1
                ok, _ = sc_database().update(ItemsInCart, item_in_cart.id, item_in_cart)

            if ok:
                return "Deleted"

    return JSONResponse(
        status_code=500,
        content=dict(
            Error(
                message="Error while adding item to cart!",
            )
        )
    )