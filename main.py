from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi import FastAPI
from user_router import router as user_router
from database import get_db
 # Folder name must match exactly

app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["User"])


class user(BaseModel):
    user_id: int
    username: str
    email: str
    password: str
    phone_number: str
    role_id: int

users: List[user] = []


@app.get("/")
def home():
    db = get_db()
    return {"message": "API working!", "db": db}


@app.get("/users")
def read_root():
    return {"users": users}

@app.get("/users/{user_id}")
def read_user(user_id: int):
    for user in users:
        if user.user_id == user_id:
            return user
    return {"error": "User not found GET"}

@app.post("/users")
def create_user(user: user):
    users.append(user)
    return {"message": "User created"}

@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: user):
    for index, user in enumerate(users):
        if user.user_id == user_id:
            users[index] = updated_user
            return {"message": "User updated"}
    return {"error": "User not found PUT"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.user_id == user_id:
            del users[index]
            return {"message": "User deleted"}
    return {"error": "User not found"}
