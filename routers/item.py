from fastapi import APIRouter, Path
from models import Cart, Item, CartSummary, Error
from typing import Union, Optional

item_router = APIRouter()


@item_router.put('/item', response_model=Item, responses={'500': {'model': Error}})
def put_item(body: Item = None) -> Union[Item, Error]:
    """
    Create New Item
    """
    pass


@item_router.get(
    '/item/{itemId}',
    response_model=Item,
    responses={'404': {'model': Error}, '500': {'model': Error}},
)
def get_item_item_id(item_id: int = Path(..., alias='itemId')) -> Union[Item, Error]:
    """
    Retrieve Item Description
    """
    pass


@item_router.post(
    '/item/{itemId}',
    response_model=Item,
    responses={'404': {'model': Error}, '500': {'model': Error}},
)
def post_item_item_id(
    item_id: int = Path(..., alias='itemId'), body: Item = None
) -> Union[Item, Error]:
    """
    Update Item Description
    """
    pass


@item_router.delete(
    '/item/{itemId}',
    response_model=None,
    responses={'404': {'model': Error}, '500': {'model': Error}},
)
def delete_item_item_id(item_id: int = Path(..., alias='itemId')) -> Optional[Error]:
    """
    Delete Item
    """
    pass
