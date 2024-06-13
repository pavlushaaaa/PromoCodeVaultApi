import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.services.datetime_format import datetime_to_string
from sqlalchemy.orm import relationship

from app.database.models import Base


class VoucherModel(Base):
    __tablename__ = "vouchers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    name = Column(String(20))
    description = Column(String(255))
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    active = Column(Boolean, default=False)
    number_of_generated_codes = Column(Integer, default=0)
    discount_value = Column(Integer)
    discount_type = Column(String)

    voucher_codes = relationship("VoucherCodeModel", back_populates="voucher")

    def to_dict(self):
        return {
            "id": self.id,
            "created_at": datetime_to_string(self.created_at),
            "name": self.name,
            "description": self.description,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "active": self.active,
            "discount_value": self.discount_value,
            "discount_type": self.discount_type,
            "number_of_generated_codes": self.number_of_generated_codes
        }


class VoucherCodeModel(Base):
    __tablename__ = "voucher_codes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    voucher_id = Column(Integer, ForeignKey("vouchers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    code = Column(UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime, default=datetime.utcnow)
    last_retrieved_at = Column(DateTime)
    voucher = relationship("VoucherModel", back_populates="voucher_codes")

    code_metadata = Column(JSON, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "voucher_id": self.voucher_id,
            "created_at": datetime_to_string(self.created_at),
            "code": str(self.code) if self.code else None,
            "used": self.used,
            "used_at": datetime_to_string(self.used_at) if self.used_at else None,
            "last_retrieved_at": datetime_to_string(self.last_retrieved_at) if self.last_retrieved_at else None,
            "discount_value": self.voucher.discount_value,
            "discount_type": self.voucher.discount_type,
            "metadata": self.code_metadata,
        }

