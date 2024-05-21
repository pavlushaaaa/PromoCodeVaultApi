from pydantic import BaseModel


class DefaultSuccessResponse(BaseModel):
    msg: str = "ok"