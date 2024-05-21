from pydantic import BaseModel
from datetime import datetime

class VoucherIdSchema(BaseModel):
    voucher_id: int


class VoucherSchema(BaseModel):
    id: int
    created_at: datetime
    name: str
    description: str
    user_id: int
    product_id: int


class VoucherCreateSchema(BaseModel):
    name: str
    description: str
    product_id: int



