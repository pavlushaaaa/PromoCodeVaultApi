from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


from .user import UserModel
from .product import ProductModel
from .voucher import VoucherModel, VoucherCodeModel
from .token import TokenModel


