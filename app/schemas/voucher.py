from pydantic import BaseModel
from datetime import datetime

class VoucherIdSchema(BaseModel):
    voucher_id: int


class VoucherSchema(BaseModel):
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



