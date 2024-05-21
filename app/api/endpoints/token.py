from app.schemas.token import TokenSchema
from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.core.settings import settings
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database.models.user import UserModel
from app.schemas.user import UserSchema
from app.services.auth import create_access_token, get_current_user, authenticate_user

router = APIRouter()


@router.post("/token", response_model=TokenSchema, tags=["tokens"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserSchema, tags=["tokens"])
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user
