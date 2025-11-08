from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class DropBase(BaseModel):
    name: str
    description: str | None = None
    total_quantity: int
    claim_start_at: datetime
    claim_end_at: datetime
    is_active: bool = True

class DropCreate(DropBase):
    pass

class DropUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    total_quantity: int | None = None
    claim_start_at: datetime | None = None
    claim_end_at: datetime | None = None
    is_active: bool | None = None

class DropOut(DropBase):
    id: int

    model_config = {"from_attributes": True}