from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import VoucherModel, UserModel
from app.schemas.voucher import VoucherSchema, VoucherCreateSchema, VoucherIdSchema
from app.schemas import DefaultSuccessResponse
from app.services.auth import get_current_user

router = APIRouter()

@router.get("/voucher/{voucher_id}", response_model=VoucherSchema, tags=["vouchers"])
def get_voucher(
    voucher_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)):
    voucher = db.query(VoucherModel).filter(VoucherModel.id == voucher_id).first()
    if not voucher:
        raise HTTPException(status_code=404, detail="Voucher not found")
    if voucher.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this voucher")
    return voucher


@router.put("/voucher", response_model=VoucherSchema, tags=["vouchers"])
def update_voucher(voucher: VoucherCreateSchema, db: Session = Depends(get_db),
                   user: UserModel = Depends(get_current_user)):
    new_voucher = VoucherModel(**voucher.model_dump())
    new_voucher.user_id = user.id
    db.add(new_voucher)
    db.commit()
    db.refresh(new_voucher)
    return new_voucher

@router.post("/voucher", response_model=VoucherSchema, tags=["vouchers"])
def create_voucher(voucher: VoucherCreateSchema, db: Session = Depends(get_db),
                   user: UserModel = Depends(get_current_user)):
    new_voucher = VoucherModel(**voucher.model_dump())
    new_voucher.user_id = user.id
    db.add(new_voucher)
    db.commit()
    db.refresh(new_voucher)
    return new_voucher

@router.delete("/voucher", response_model=DefaultSuccessResponse, tags=["vouchers"])
def delete_voucher(voucher: VoucherIdSchema, db: Session = Depends(get_db),
                   user: UserModel = Depends(get_current_user)):
    db_voucher = db.query(VoucherModel).get(voucher.id)
    if db_voucher.user_id != user.id:
        raise HTTPException(detail="You do not have permission to delete this voucher", status_code=401)
    db.delete(db_voucher)
    db.commit()
    return DefaultSuccessResponse()




