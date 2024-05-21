from pydantic import BaseModel
from datetime import datetime


class ProductIdSchema(BaseModel):
    product_id: int

class ProductCreateSchema(BaseModel):
    name: str
    description: str


class ProductSchema(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime

class ProductUpdateSchema(ProductSchema, ProductIdSchema):
    pass
