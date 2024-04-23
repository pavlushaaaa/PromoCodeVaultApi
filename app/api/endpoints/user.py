from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import UserModel, TokenModel
from app.schemas.user import UserCreateSchema, UserSchema
from app.services.auth import get_password_hash, verify_password, create_access_token, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime

router = APIRouter()


@router.post("/users/", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserModel(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Token expiry time
    access_token_expires = timedelta(minutes=30)  # Adjust as needed
    # Create a new access token
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    # Calculate the expiration time for the database record
    expires_at = datetime.utcnow() + access_token_expires
    # Create and save the token record to the database
    new_token = TokenModel(
        token=access_token,
        user_id=user.id,
        created_at=datetime.utcnow(),
        expires_at=expires_at,
        revoked=False,
        revoked_at=None
    )
    db.add(new_token)
    db.commit()
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    active_tokens = db.query(TokenModel).filter(TokenModel.user_id == user.id, TokenModel.revoked_at.is_(None)).all()
    if active_tokens:
        for token in active_tokens:
            token.revoked_at = datetime.utcnow()
        db.commit()
        return {"message": "User logged out successfully, all tokens revoked."}
    return {"message": "No active session found or all sessions already revoked."}

