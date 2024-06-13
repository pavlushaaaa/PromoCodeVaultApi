from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import UserModel, VoucherModel, VoucherCodeModel, ProductModel
from app.schemas.analytics import VouchersListSchema, VoucherCodesListSchema, VoucherAnalytics, ProductsListSchema
from app.services.auth import get_current_user

router = APIRouter()


@router.get("/vouchers", response_model=VouchersListSchema, tags=["analytics"])
def get_all_vouchers(
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)):
    vouchers = db.query(VoucherModel).all()
    vouchers_list = VouchersListSchema(vouchers=[voucher.to_dict() for voucher in vouchers])
    return vouchers_list


@router.get("/voucher_codes", response_model=VoucherCodesListSchema, tags=["analytics"])
def get_all_voucher_codes(
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)):
    voucher_codes = db.query(VoucherCodeModel).all()
    voucher_codes_list = VoucherCodesListSchema(
        voucher_codes=[voucher_code.to_dict() for voucher_code in voucher_codes])
    return voucher_codes_list

@router.get("/products", response_model=ProductsListSchema, tags=["analytics"])
def get_all_products(
        db: Session = Depends(get_db),
        user: UserModel = Depends(get_current_user)):
    products = db.query(ProductModel).all()
    products_list = ProductsListSchema(
        products=[product.to_dict() for product in products])
    return products_list


@router.get("/general_analytics", tags=["analytics"], response_model=VoucherAnalytics)
def get_all_voucher_codes(db: Session = Depends(get_db),
                          user: UserModel = Depends(get_current_user)):
    total_voucher_codes = db.query(VoucherCodeModel).count()
    total_unused_voucher_codes = db.query(VoucherCodeModel).filter(VoucherModel.used == False).count()
    total_used_voucher_codes = db.query(VoucherCodeModel).filter(VoucherModel.used == True).count()
    total_products = db.query(ProductModel).count()
    total_vouchers = db.query(VoucherModel).count()
    total_active_vouchers = db.query(VoucherModel).filter(VoucherModel.active == True).count()
    total_inactive_vouchers = db.query(VoucherModel).filter(VoucherModel.active == False).count()

    return VoucherAnalytics(
        total_voucher_codes=total_voucher_codes,
        total_unused_voucher_codes=total_unused_voucher_codes,
        total_used_voucher_codes=total_used_voucher_codes,
        total_products=total_products,
        total_vouchers=total_vouchers,
        total_active_vouchers=total_active_vouchers,
        total_inactive_vouchers=total_inactive_vouchers
    )
