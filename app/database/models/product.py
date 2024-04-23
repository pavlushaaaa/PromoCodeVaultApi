from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.models import Base
from datetime import datetime


class ProductModel(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    name = Column(String(20))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))

