from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from models import Cart, Item, CartSummary, Error
from typing import Union, Optional

from services import sc_database

item_router = APIRouter()


@item_router.put('/item', response_model=Item, responses={'500': {'model': Error}})
def put_item(item: Item = None) -> Union[Item, Error]:
    """
    Create New Item
    """
    ok, db_item = sc_database().create(item)
    
    if ok:
        return db_item
    else:
        return JSONResponse(
            status_code=500,
            content=dict(
                Error(
                    message="Error while creating item",
                )
            )
        )


@item_router.get(
    '/item/{itemId}',
    response_model=Item,
    responses={'404': {'model': Error}, '500': {'model': Error}},
)
def get_item_item_id(item_id: int = Path(..., alias='itemId')) -> Union[Item, Error]:
    """
    Retrieve Item Description
    """
    ok, db_item = sc_database().retrieve(Item, id=item_id)
    
    if ok:
        return db_item
    elif db_item == None:
        return JSONResponse(
            status_code=404,
            content=dict(
                Error(
                    message=f"Item with ID {item_id} does not exist",
                )
            )
        )
    else:
        return JSONResponse(
            status_code=500,
            content=dict(
                Error(
                    message=f"Error while retrieving item: {db_item}",
                )
            )
        )


@item_router.post(
    '/item/{itemId}',
    response_model=Item,
    responses={'404': {'model': Error}, '500': {'model': Error}},
)
def post_item_item_id(
    item_id: int = Path(..., alias='itemId'), item: Item = None
) -> Union[Item, Error]:
    """
    Update Item Description
    """
    ok, db_item = sc_database().update(Item, id=item_id, content=item)
    
    if ok:
        if db_item == None:
            return JSONResponse(
                status_code=404,
                content=dict(
                    Error(
                        message=f"Item with ID {item_id} does not exist",
                    )
                )
            )
        return db_item
    else:
        return JSONResponse(
            status_code=500,
            content=dict(
                Error(
                    message="Error while updating item",
                )
            )
        )


@item_router.delete(
    '/item/{itemId}',
    response_model=None,
    responses={'404': {'model': Error}, '500': {'model': Error}},
)
def delete_item_item_id(item_id: int = Path(..., alias='itemId')) -> Optional[Error]:
    """
    Delete Item
    """
    ok, num_deleted = sc_database().delete(Item, id=item_id)
    
    if ok:
        if num_deleted == 1:
            return "Deleted"
        elif num_deleted == 0:
            return JSONResponse(
            status_code=404,
            content=dict(
                Error(
                    message=f"Item with ID {item_id} does not exist",
                )
            )
        )
    return JSONResponse(
        status_code=500,
        content=dict(
            Error(
                message="Error while deleting item",
            )
        )
    )
