from pydantic import BaseModel
from typing import Literal


class DiscountSchema(BaseModel):
    discount_type: Literal['specific', 'percentage']
    discount_value: int
