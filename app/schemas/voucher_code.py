from pydantic import BaseModel
from typing import Optional
from app.schemas.discount import DiscountSchema

class VoucherCodeIdSchema(BaseModel):
    voucher_code_id: int


class VoucherCodeSchema(DiscountSchema):
    id: int
    voucher_id: int
    created_at: Optional[str] = None
    code: str
    used: bool
    used_at: Optional[str] = None
    last_retrieved_at: Optional[str] = None
    metadata: Optional[dict] = None

