# app/schemas/token.py

from pydantic import BaseModel

class TokenData(BaseModel):
    email: str | None = None