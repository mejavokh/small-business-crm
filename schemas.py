from pydantic import BaseModel, ConfigDict
from datetime import datetime

# --------- schemas for user ---------
class UserCreate(BaseModel):
    name: str
    phone: str
    password: str
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

# --------- schemas for service ---------
class ServiceCreate(BaseModel):
    name: str
    price: float
    duration: int

class ServiceUpdate(BaseModel):
    name: str | None=None
    price: float | None=None
    duration: int | None=None

class ServiceResponse(BaseModel):
    id: int
    name: str
    price: float
    duration: int

    model_config = ConfigDict(from_attributes=True)

# --------- schemas for booking ----------
class BookingCreate(BaseModel):
    order_id: int
    employee_id: int
    scheduled_at: datetime
    status: str

class BookingUpdate(BaseModel):
    employee_id: int | None = None
    scheduled_at: datetime | None = None
    status: str | None = None

class BookingResponse(BaseModel):
    id: int
    order_id: int
    employee_id: int
    scheduled_at: datetime
    status: str

    model_config = ConfigDict(from_attributes=True)

# --------- schemas for order ----------
class OrderCreate(BaseModel):
    client_id: int
    service_id: int
    status: str
    created_at: datetime

class OrderUpdate(BaseModel):
    client_id: int | None = None
    service_id: int | None = None
    status: str | None = None
    created_at: datetime | None = None

class OrderResponse(BaseModel):
    id: int
    client_id: int
    service_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ---------- schemas for payment ----------
class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    method: str

class PaymentUpdate(BaseModel):
    booking_id: int | None = None
    amount: float | None = None
    method: str | None = None

class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: float
    method: str

    model_config = ConfigDict(from_attributes=True)

class RefreshToken(BaseModel):
    refresh_token: str
