from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


from app.database.database import get_db
from app.database.models import UserModel, VoucherModel, VoucherCodeModel
from app.schemas.analytics import VouchersListSchema, VoucherCodesListSchema
from app.services.auth import get_current_user


router = APIRouter()


@router.get("/vouchers", response_model=VouchersListSchema, tags=["analytics"])
def get_all_vouchers(
    db: Session = Depends(get_db)):
    # user: UserModel = Depends(get_current_user)):

    vouchers = db.query(VoucherModel).all()
    vouchers_list = VouchersListSchema(vouchers=[voucher.to_dict() for voucher in vouchers])
    return vouchers_list

@router.get("/voucher_codes", response_model=VoucherCodesListSchema, tags=["analytics"])
def get_all_voucher_codes(
    db: Session = Depends(get_db)):
    # user: UserModel = Depends(get_current_user)):

    voucher_codes = db.query(VoucherCodeModel).all()
    voucher_codes_list = VoucherCodesListSchema(voucher_codes=[voucher_code.to_dict() for voucher_code in voucher_codes])
    return voucher_codes_list
