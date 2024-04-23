from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.database.models import Base
from datetime import datetime
import uuid

class VoucherModel(Base):
    __tablename__ = "vouchers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    name = Column(String(20))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))


class VoucherCodeModel(Base):
    __tablename__ = "voucher_codes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    voucher_id = Column(Integer, ForeignKey("vouchers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    code = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime, default=datetime.utcnow)
    last_retrieved_at = Column(DateTime)


