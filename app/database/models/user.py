from sqlalchemy import Column, Integer, String, DateTime
from app.database.models import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    email = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    password_hash = Column(String(255))

    # Relationship to TokenModel
    tokens = relationship("TokenModel", back_populates="user", cascade="all, delete-orphan")

