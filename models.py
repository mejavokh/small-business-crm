from database import Base, engine
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, func


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Float)
    duration: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:
        return (f"Service(id={self.id}, name={self.name!r}, "
                f"price={self.price!r}, duration={self.duration!r})")

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(20))
    password_hash: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return (f"User(id={self.id}, name={self.name!r}, "
                f"phone={self.phone!r}, role={self.role!r})")

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"))
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    def __repr__(self) -> str:
        return (f"Order(id={self.id}, client_id={self.client_id}, "
                f"service_id={self.service_id}, status={self.status!r},"
                f"created_at={self.created_at!r})")

class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    scheduled_at: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return (f"Book(id={self.id}, order_id={self.order_id}, "
                f"employee_id={self.employee_id}, scheduled_at={self.scheduled_at!r},"
                f"status={self.status!r})")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"))
    amount: Mapped[float] = mapped_column(Float)
    paid_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    method: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return (f"Payment(id={self.id}, booking_id={self.booking_id}, "
                f"amount={self.amount!r}, paid_at={self.paid_at!r},"
                f"method={self.method})")

