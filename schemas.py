from pydantic import BaseModel, ConfigDict

class UserCreate(BaseModel):
    name: str
    phone: str
    password_hash: str
    role: str

class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    role: str | None = None

class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    role: str

    model_config = ConfigDict(from_attributes=True)