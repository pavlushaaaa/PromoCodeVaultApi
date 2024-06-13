from pydantic import BaseModel
from typing import List
from app.schemas.voucher import VoucherSchema
from app.schemas.voucher_code import VoucherCodeSchema
from app.schemas.product import ProductSchema



class VouchersListSchema(BaseModel):
    vouchers: List[VoucherSchema]

class VoucherCodesListSchema(BaseModel):
    voucher_codes: List[VoucherCodeSchema]

class ProductsListSchema(BaseModel):
    products: List[ProductSchema]


class VoucherAnalytics(BaseModel):
    total_voucher_codes: int
    total_unused_voucher_codes: int
    total_used_voucher_codes: int
    total_products: int
    total_vouchers: int
    total_active_vouchers: int
    total_inactive_vouchers: int