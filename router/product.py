from turtle import width
from urllib import response
from fastapi import APIRouter, Depends, Response
from db.database import get_db
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse

router = APIRouter(
    prefix='/product',
    tags=['product']
)

product = ['boat', 'watch', 'ink']


@router.get('/all')
def get_all_products():
    # return product
    data = " ".join(product)
    return Response(content=data, media_type="text/plain")


@router.get('/{id}', responses={
    200: {
        "content": {
            "text/html": {
                "example": "<div>Product</div>"
            }
        },
        "description": "Returns the HTML for an object"
    },
    404: {
        "content": {
            "text/plain": {
                "Product not available"
            }
        },
        "description": "A cleartext error message"
    },
})
def get_product(id: int):
    if id > len(product):
        out = "Product not available"
        return Response(status_code=404, content=out, media_type="text/plain")
    prod = product[id]
    out = f"""
    <head>
    <style>
        .product{{
            width: 500px;
            background-color: blue;
        }}
    </style>
    </head>
    <div class="product"> {prod} </div>
    """

    return HTMLResponse(content=out, media_type="text/html")
