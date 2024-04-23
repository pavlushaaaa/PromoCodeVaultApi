from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from .product import ProductModel
from .token import TokenModel
from .user import UserModel
from .voucher import VoucherCodeModel, VoucherModel
