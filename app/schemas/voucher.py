from pydantic import BaseModel
from app.schemas.discount import DiscountSchema

class VoucherIdSchema(BaseModel):
    voucher_id: int


class VoucherSchema(DiscountSchema):
    id: int
    created_at: str
    name: str
    description: str
    user_id: int
    product_id: int
    active: bool


class VoucherCreateSchema(BaseModel):
    name: str
    description: str
    product_id: int



