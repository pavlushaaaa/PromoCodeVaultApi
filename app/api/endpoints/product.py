from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ProductModel, UserModel
from app.schemas import DefaultSuccessResponse
from app.schemas.product import ProductCreateSchema, ProductSchema, ProductIdSchema, ProductUpdateSchema
from app.services.auth import get_current_user

router = APIRouter()


@router.get("/product/{product_id}", response_model=ProductSchema, tags=["products"])
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_current_user)):
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this product")
    return product


@router.post("/product", response_model=ProductSchema, tags=["products"])
def create_product(product: ProductCreateSchema, db: Session = Depends(get_db),
                   user: UserModel = Depends(get_current_user)):
    new_product = ProductModel(**product.model_dump())
    new_product.user_id = user.id
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


@router.delete("/product", response_model=ProductSchema, tags=["products"])
def delete_product(product: ProductIdSchema, db: Session = Depends(get_db),
                   user: UserModel = Depends(get_current_user)):
    db_product = db.query(ProductModel).get(product.id)
    if db_product.user_id != user.id:
        raise HTTPException(detail="You do not have permission to delete this product", status_code=401)
    db.delete(db_product)
    db.commit()
    return DefaultSuccessResponse()


@router.put("/product", response_model=ProductSchema, tags=["products"])
def update_product(product: ProductUpdateSchema, db: Session = Depends(get_db),
                   user: UserModel = Depends(get_current_user)):
    db_product = db.query(ProductModel).get(product.id)

    if db_product.user_id != user.id:
        raise HTTPException(detail="You do not have permission to amend this product", status_code=401)

    db_product.description = product.description
    db_product.name = product.name
    db_product.price = product.price

    db.commit()
    db.refresh(db_product)
    return db_product
