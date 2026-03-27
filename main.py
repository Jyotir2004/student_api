from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from routes.auth_routes import router as auth_router

app = FastAPI()

app.include_router(auth_router)


app = FastAPI()
from routes.auth_routes import router as auth_router

app = FastAPI()

app.include_router(auth_router)

class user(BaseModel):
    user_id: int
    username: str
    email: str
    password: str
    phone_number: str
    role_id: int

users: List[user] = []

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
