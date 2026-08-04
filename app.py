from fastapi import FastAPI, HTTPException
from typing import List

from database import Session
from crud import get_all_users, create_user, get_user_by_id, update_user, delete_user
from schemas import UserResponse, UserCreate, UserUpdate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, CRM!"}

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