from dataclasses import dataclass
from enum import Enum

@dataclass
class Client:
    id: int
    name: str
    phone: str

class OrderStatus(Enum):
    PENDING = "в ожидании"
    ACCEPTED = "принята"
    CANCELLED = "отменена"

@dataclass
class Order:
    order_id: int
    client_id: int
    date: str
    description: str
    status: OrderStatus




