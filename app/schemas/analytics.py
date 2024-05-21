from pydantic import BaseModel
from typing import List
from app.schemas.voucher import VoucherSchema
from app.schemas.voucher_code import VoucherCodeSchema



class VouchersListSchema(BaseModel):
    vouchers: List[VoucherSchema]

class VoucherCodesListSchema(BaseModel):
    voucher_codes: List[VoucherCodeSchema]