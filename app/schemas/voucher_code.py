from pydantic import BaseModel
from typing import Optional

class VoucherCodeIdSchema(BaseModel):
    voucher_code_id: int


class VoucherCodeSchema(BaseModel):
    id: int
    voucher_id: int
    created_at: Optional[str] = None
    code: str
    used: bool
    used_at: Optional[str] = None
    last_retrieved_at: Optional[str] = None

