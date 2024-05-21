from pydantic import BaseModel


class DiscountSchema(BaseModel):
    discount_type: str
    discount_value: int
