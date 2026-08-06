from fastapi import FastAPI, HTTPException
from typing import List

from sqlalchemy.ext.horizontal_shard import set_shard_id
from sqlalchemy.orm import sessionmaker

from database import Session
from crud import *
from schemas import *

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, CRM!"}

# ---------- эндпоинты для user ----------
@app.get("/clients", response_model=List[UserResponse])
def get_clients():
    session = Session()
    users = get_all_users(session)
    session.close()
    return users

@app.post("/clients", response_model=UserResponse)
def create_client(user_data: UserCreate):
    session = Session()
    new_user = create_user(session,
                           name=user_data.name, phone=user_data.phone,
                           password_hash=user_data.password_hash, role=user_data.role)
    session.close()
    return new_user

@app.get("/clients/{client_id}", response_model=UserResponse)
def get_client(client_id: int):
    session = Session()
    user = get_user_by_id(session, client_id)
    session.close()

    if user is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return user

@app.patch("/clients/{client_id}", response_model=UserResponse)
def update_user_by_id(client_id: int, user_data: UserUpdate):
    session = Session()
    result = update_user(session, user_id=client_id, name=user_data.name,
                       phone=user_data.phone, role=user_data.role)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="User not found")

    user = get_user_by_id(session, client_id)
    session.close()

    return user

@app.delete("/clients/{client_id}", status_code=204)
def delete_client(client_id: int):
    session = Session()
    result = delete_user(session, client_id)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="User not found")

    session.close()

# --------- Эндпоинты для service ---------
@app.get("/services", response_model=List[ServiceResponse])
def get_services():
    session = Session()
    services = get_all_services(session)
    session.close()

    return services

@app.get("/services/{service_id}", response_model=ServiceResponse)
def get_service(service_id):
    session = Session()
    service = get_service_by_id(session, service_id)
    session.close()

    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    return service

@app.post("/services", response_model=ServiceResponse)
def create_service_endpoint(service_data: ServiceCreate):
    session = Session()
    new_service = create_service(session, name=service_data.name,
                                 price=service_data.price, duration=service_data.duration)
    session.close()

    return new_service

@app.patch("/services/{service_id}", response_model=ServiceResponse)
def update_service_by_id(service_id: int, service_data: ServiceUpdate):
    session = Session()
    result = update_service(session, service_id = service_id, name=service_data.name,
                            price=service_data.price, duration=service_data.duration)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="Service not found")

    service = get_service_by_id(session, service_id)
    session.close()

    return service

@app.delete("/services/{service_id}", status_code=204)
def delete_service_endpoint(service_id: int):
    session = Session()
    result = delete_service(session, service_id)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="Service not found")

    session.close()

# -------- Эндпоинты для booking ---------
@app.get("/bookings",  response_model=List[BookingResponse])
def get_bookings():
    session = Session()
    bookings = get_all_bookings(session)
    session.close()

    return bookings

@app.post("/bookings", response_model=BookingResponse)
def create_booking_endpoint(booking_data: BookingCreate):
    session = Session()

    order = get_order_by_id(session, booking_data.order_id)
    if order is None:
        session.close()
        raise HTTPException(status_code=404, detail="Order not found")

    employee = get_user_by_id(session, booking_data.employee_id)
    if employee is None:
        session.close()
        raise HTTPException(status_code=404, detail="Employee not found")

    new_booking = create_booking(session, order_id=booking_data.order_id, scheduled_at=booking_data.scheduled_at,
                                 status=booking_data.status, employee_id=booking_data.employee_id)
    session.close()

    return new_booking

@app.get("/bookings/{booking_id}", response_model=BookingResponse)
def get_booking_by_id_endpoint(booking_id: int):
    session = Session()
    booking = get_booking_by_id(session, booking_id)
    session.close()

    if booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")

    return booking

@app.patch("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking_endpoint(booking_id: int, booking_data: BookingUpdate):
    session = Session()

    if booking_data.order_id is not None:
        order = get_order_by_id(session, booking_data.order_id)
        if order is None:
            session.close()
            raise HTTPException(status_code=404, detail="Order not found")

    if booking_data.employee_id is not None:
        employee = get_user_by_id(session, booking_data.employee_id)
        if employee is None:
            session.close()
            raise HTTPException(status_code=404, detail="Employee not found")

    result = update_booking(session, booking_id, order_id=booking_data.order_id,
                            employee_id=booking_data.employee_id, status=booking_data.status,
                            scheduled_at=booking_data.scheduled_at)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="Booking not found")

    booking = get_booking_by_id(session, booking_id)
    session.close()

    return booking

@app.delete("/bookings/{booking_id}", status_code=204)
def delete_booking_endpoint(booking_id: int):
    session = Session()
    result = delete_booking(session, booking_id)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="Booking not found")

    session.close()

# ---------- Эндпоинты для order ----------
@app.get("/orders", response_model=List[OrderResponse])
def get_orders():
    session = Session()
    orders = get_all_orders(session)
    session.close()

    return orders

@app.post("/orders", response_model=OrderResponse)
def create_order_endpoint(order_data: OrderCreate):
    session = Session()

    if order_data.service_id is not None:
        service = get_service_by_id(session, order_data.service_id)
        if service is None:
            session.close()
            raise HTTPException(status_code=404, detail="Service not found")

    if order_data.client_id is not None:
        client = get_user_by_id(session, order_data.client_id)
        if client is None:
            session.close()
            raise HTTPException(status_code=404, detail="User not found")

    new_order = create_order(session,
                             client_id=order_data.client_id, service_id=order_data.service_id,
                             status=order_data.status, created_at=order_data.created_at)
    session.close()

    return new_order

@app.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int):
    session = Session()
    order = get_order_by_id(session, order_id)
    session.close()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order

@app.patch("/orders/{order_id}", response_model=OrderResponse)
def update_order_endpoint(order_id: int, order_data: OrderUpdate):
    session = Session()

    if order_data.service_id is not None:
        service = get_service_by_id(session, order_data.service_id)
        if service is None:
            session.close()
            raise HTTPException(status_code=404, detail="Service not found")

    if order_data.client_id is not None:
        client = get_user_by_id(session, order_data.client_id)
        if client is None:
            session.close()
            raise HTTPException(status_code=404, detail="User not found")

    result = update_order(session, order_id=order_id, client_id=order_data.client_id,
                          service_id=order_data.service_id, status=order_data.status,
                          created_at=order_data.created_at)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="Order not found")

    order = get_order_by_id(session, order_id)
    session.close()

    return order

@app.delete("/orders/{order_id}", status_code=204)
def delete_order_endpoint(order_id: int):
    session = Session()
    result = delete_order(session, order_id)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="Order not found")

    session.close()

# ---------- Эндпоинты для payment ----------
@app.get("/payments", response_model=List[PaymentResponse])
def get_payments():
    session = Session()
    payments = get_all_payments(session)
    session.close()

    return payments

@app.post("/payments", response_model=PaymentResponse)
def create_payment_endpoint(payment_data: PaymentCreate):
    session = Session()

    if payment_data.booking_id is not None:
        booking = get_booking_by_id(session, payment_data.booking_id)
        if booking is None:
            session.close()
            raise HTTPException(status_code=404, detail="Booking not found")

    new_payment = create_payment(session,
                                 booking_id=payment_data.booking_id,
                                 amount=payment_data.amount,
                                 method=payment_data.method)
    session.close()
    return new_payment

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int):
    session = Session()
    payment = get_payment_by_id(session, payment_id)
    session.close()

    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment

@app.patch("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment_endpoint(payment_id: int, payment_data: PaymentUpdate):
    session = Session()

    if payment_data.booking_id is not None:
        booking = get_booking_by_id(session, payment_data.booking_id)
        if booking is None:
            session.close()
            raise HTTPException(status_code=404, detail="Booking not found")

    result = update_payment(session, payment_id=payment_id,
                            booking_id=payment_data.booking_id,
                            amount=payment_data.amount,
                            method=payment_data.method)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="Payment not found")

    payment = get_payment_by_id(session, payment_id)
    session.close()

    return payment

@app.delete("/payments/{payment_id}", status_code=204)
def delete_payment_endpoint(payment_id: int):
    session = Session()
    result = delete_payment(session, payment_id)

    if not result:
        session.close()
        raise HTTPException(status_code=404, detail="Payment not found")

    session.close()