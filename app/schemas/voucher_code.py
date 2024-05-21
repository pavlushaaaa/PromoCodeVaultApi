from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class VoucherCodeIdSchema(BaseModel):
    voucher_code_id: int


class VoucherCodeSchema(BaseModel):
    id: int
    voucher_id: int
    created_at: datetime
    code: UUID
    used: bool
    used_at: datetime
    last_retrieval_at: datetime

