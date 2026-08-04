from sqlalchemy import select
from sqlalchemy.orm import Session
from models import User, Order, Service, Booking, Payment


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