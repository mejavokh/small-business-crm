from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from models import User, Order, Service, Booking, Payment

# --------- crud for user ---------
def create_user(session: Session, name: str, phone: str, password_hash: str, role: str) -> User:
    user = User(
        name = name,
        phone = phone,
        password_hash = password_hash,
        role = role
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user

def get_user_by_id(session: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    user = session.execute(stmt).scalar_one_or_none()

    return user

def get_all_users(session: Session) -> list[User]:
    stmt = select(User)
    result = session.execute(stmt)
    users = result.scalars().all()

    return list(users)

def update_user(session: Session, user_id: int,
                name: str | None=None, phone: str | None=None, role: str | None=None) -> bool:
    stmt = select(User).where(User.id == user_id)
    user = session.execute(stmt).scalar_one_or_none()

    if user:
        if name is not None and name !="":
            user.name = name
        if phone is not None and phone !="":
            user.phone = phone
        if role is not None and role !="":
            user.role =role
        session.commit()
        session.refresh(user)
        return True

    return False

def delete_user(session: Session, user_id: int) -> bool:
    stmt = select(User).where(User.id == user_id)
    user = session.execute(stmt).scalar_one_or_none()

    if user:
        session.delete(user)
        session.commit()
        return True

    return False

def get_orders_with_details(session: Session) -> list[tuple[Order, User, Service]]:
    stmt = (
        select(Order, User, Service)
        .join(User, Order.client_id == User.id)
        .join(Service, Order.service_id == Service.id)
    )
    result = session.execute(stmt)
    return [(order, user, service) for order, user, service in result]

def get_booking_with_details(session: Session) -> list[tuple[Booking, Order, Service]]:
    stmt = (
        select(Booking, Order, Service)
        .join(Order, Booking.order_id == Order.id)
        .join(Service, Order.service_id == Service.id)
    )
    result = session.execute(stmt)
    return [(order, user, service) for order, user, service in result]

def process_payment(session: Session, booking_id: int, amount: float, method: str) -> bool:
    try:
        booking = session.execute(
            select(Booking).where(Booking.id == booking_id)
        ).scalar_one_or_none()

        if booking is None:
            return False

        payment = Payment(booking_id=booking_id, amount=amount, method=method)
        session.add(payment)
        booking.status = "completed"

        session.commit()
        return True
    except Exception:
        session.rollback()
        return False

# ---------- crud for service ----------
def create_service(session: Session, name: str, price: float, duration: int) -> Service:
    service = Service(name=name, price=price, duration=duration)
    session.add(service)
    session.commit()
    session.refresh(service)

    return service

def get_service_by_id(session: Session, service_id: int) -> Service | None:
    stmt = select(Service).where(Service.id == service_id)

    return session.execute(stmt).scalar_one_or_none()

def get_all_services(session: Session) -> list[Service]:
    stmt = select(Service)
    result = session.execute(stmt)

    return list(result.scalars().all())

def update_service(session: Session, service_id: int,
                   name: str | None=None, price: float | None=None, duration: int | None=None) -> bool:
    stmt = select(Service).where(Service.id == service_id)
    service = session.execute(stmt).scalar_one_or_none()

    if service:
        if name is not None and name != "":
            service.name = name
        if price is not None:
            service.price = price
        if duration is not None:
            service.duration = duration
        session.commit()
        session.refresh(service)

        return True

    return False

def delete_service(session: Session, service_id: int) -> bool:
    stmt = select(Service).where(Service.id == service_id)
    service = session.execute(stmt).scalar_one_or_none()

    if service:
        session.delete(service)
        session.commit()
        return True

    return False

# ---------- crud for booking ---------
def create_booking(session: Session, order_id: int,
                   scheduled_at: datetime, status: str, employee_id: int) -> Booking:
    booking = Booking(
        order_id = order_id, scheduled_at=scheduled_at, status=status, employee_id=employee_id
    )
    session.add(booking)
    session.commit()
    session.refresh(booking)

    return booking

def get_booking_by_id(session: Session, booking_id: int) -> Booking | None:
    stmt = select(Booking).where(Booking.id == booking_id)
    booking = session.execute(stmt).scalar_one_or_none()

    return booking

def get_all_bookings(session: Session) -> list[Booking]:
    stmt = select(Booking)
    result = session.execute(stmt)
    bookings = result.scalars().all()

    return list(bookings)

def update_booking(session: Session, booking_id: int,
                   order_id: int | None = None, employee_id: int | None = None,
                   status: str | None = None, scheduled_at: datetime | None = None) -> bool:
    stmt = select(Booking).where(Booking.id == booking_id)
    booking = session.execute(stmt).scalar_one_or_none()

    if booking:
        if order_id is not None:
            booking.order_id = order_id
        if employee_id is not None:
            booking.employee_id = employee_id
        if scheduled_at is not None:
            booking.scheduled_at = scheduled_at
        if status is not None and status !="":
            booking.status = status

        session.commit()
        session.refresh(booking)
        return True

    return False


def delete_booking(session: Session, booking_id: int) -> bool:
    stmt = select(Booking).where(Booking.id == booking_id)
    booking = session.execute(stmt).scalar_one_or_none()

    if booking:
        session.delete(booking)
        session.commit()
        return True

    return False

# ---------- crud for order ----------
def create_order(session: Session, client_id: int, service_id: int,
                 status: str, created_at: datetime) -> Order:
    order = Order(
        client_id = client_id,
        service_id = service_id,
        status = status,
        created_at = created_at
    )

    session.add(order)
    session.commit()
    session.refresh(order)

    return order

def get_order_by_id(session: Session, order_id: int) -> Order | None:
    stmt = select(Order).where(Order.id == order_id)
    order = session.execute(stmt).scalar_one_or_none()

    return order

def get_all_orders(session: Session) -> list[Order]:
    stmt = select(Order)
    result = session.execute(stmt)
    orders = result.scalars().all()

    return list(orders)

def update_order(session: Session, order_id: int,
                 client_id: int | None = None, service_id: int | None = None,
                 status: str | None = None, created_at: datetime | None = None) -> bool:
    stmt = select(Order).where(Order.id == order_id)
    order = session.execute(stmt).scalar_one_or_none()

    if order:
        if client_id is not None:
            order.client_id = client_id
        if service_id is not None:
            order.service_id = service_id
        if status is not None and status !="":
            order.status = status
        if created_at is not None:
            order.created_at = created_at

        session.commit()
        session.refresh(order)
        return True

    return False

def delete_order(session: Session, order_id: int) -> bool:
    stmt = select(Order).where(Order.id == order_id)
    order = session.execute(stmt).scalar_one_or_none()

    if order:
        session.delete(order)
        session.commit()
        return True

    return False

# ---------- crud for payment ----------
def create_payment(session: Session, booking_id: int, amount: float, method: str) -> Payment:
    payment = Payment(
        booking_id = booking_id,
        amount = amount,
        paid_at = datetime.now(),
        method = method
    )
    session.add(payment)
    session.commit()
    session.refresh(payment)

    return payment

def get_payment_by_id(session: Session, payment_id: int) -> Payment | None:
    stmt = select(Payment).where(Payment.id == payment_id)
    payment = session.execute(stmt).scalar_one_or_none()

    return payment

def get_all_payments(session: Session) -> list[Payment]:
    stmt = select(Payment)
    result = session.execute(stmt)
    payments = result.scalars().all()

    return list(payments)

def update_payment(session: Session, payment_id: int,
                   booking_id: int | None=None, amount: float | None=None,
                   method: str | None=None) -> bool:
    stmt = select(Payment).where(Payment.id==payment_id)
    payment = session.execute(stmt).scalar_one_or_none()

    if payment:
        if booking_id is not None:
            payment.booking_id = booking_id
        if amount is not None:
            payment.amount = amount
        if method is not None and method !="":
            payment.method = method
        session.commit()
        session.refresh(payment)
        return True

    return False

def delete_payment(session: Session, payment_id: int) -> bool:
    stmt = select(Payment).where(Payment.id == payment_id)
    payment = session.execute(stmt).scalar_one_or_none()

    if payment:
        session.delete(payment)
        session.commit()
        return True

    return False

# ---------- filters ----------
def get_user_by_phone(session: Session, phone: str) -> User | None:
    stmt = select(User).where(User.phone == phone)
    return session.execute(stmt).scalar_one_or_none()
