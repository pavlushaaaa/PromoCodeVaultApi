from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.models import UserModel
from app.schemas.user import UserCreateSchema, UserSchema
from app.services.auth import get_password_hash
from app.database.database import get_db

router = APIRouter()

@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(email=user.email, password_hash=hashed_password,
                        first_name=user.first_name, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user