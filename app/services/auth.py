from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.database.database import get_db
from app.database.models.user import UserModel
from app.database.models.token import TokenModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user: UserModel, db: Session, data: dict = None, expires_delta: timedelta = None):
    if data is None:
        data = {}
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode = data.copy() | {"sub": str(user.id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    expires_at = (
        datetime.now(timezone.utc) + expires_delta if expires_delta else expire
    )
    new_token = TokenModel(
        token=encoded_jwt,
        user_id=user.id,
        created_at=datetime.now(timezone.utc),
        expires_at=expires_at,
        revoked=False,
        revoked_at=None,
    )
    db.add(new_token)
    db.commit()

    return encoded_jwt


def verify_token(token: str, db: Session, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        db_token = db.query(TokenModel).filter(TokenModel.token == token).first()
        if (
            db_token is None
            or db_token.revoked
            or db_token.expires_at < datetime.now(timezone.utc)
        ):
            raise credentials_exception

        return user_id
    except JWTError:
        raise credentials_exception


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    return user if user and verify_password(password, user.password_hash) else None


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    user_id = verify_token(token, db, credentials_exception)
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
