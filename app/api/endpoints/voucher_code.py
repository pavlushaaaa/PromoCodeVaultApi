from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import VoucherCodeModel
from app.schemas.voucher_code import VoucherCodeSchema
from app.schemas import DefaultSuccessResponse

router = APIRouter()


@router.get("/voucher-code/{code}", response_model=VoucherCodeSchema, tags=["voucher_codes"])
def get_voucher_details(
    code: str,
    db: Session = Depends(get_db)):

    voucher_code = db.query(VoucherCodeModel).filter(VoucherCodeModel.code == code).first()

    if not voucher_code:
        raise HTTPException(status_code=404, detail="Voucher not found")
    return voucher_code.to_dict()


@router.post("/voucher-code/{code}", response_model=DefaultSuccessResponse, tags=["voucher_codes"])
def use_voucher(
    code: str,
    db: Session = Depends(get_db)):

    voucher_code = db.query(VoucherCodeModel).filter(VoucherCodeModel.code == code).first()

    if not voucher_code:
        raise HTTPException(status_code=404, detail="Voucher code not found")

    if voucher_code.used:
        raise HTTPException(status_code=404, detail="Voucher code already used")

    voucher_code.used = True
    voucher_code.used_at = datetime.now()

    db.commit()

    return DefaultSuccessResponse()
