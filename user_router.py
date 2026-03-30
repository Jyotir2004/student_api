from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from auth import hash_password, verify_password, create_access_token
from models import User
from fastapi import APIRouter

from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta

router = APIRouter()




SECRET_KEY = "your_super_secret_key"  # 🔑 Change this for production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour

def create_access_token(data: dict):
    """Generate JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        raise Exception("Token expired")
    except JWTError:
        raise Exception("Invalid token")


@router.get("/test")
def test_route():
    return {"message": "User router working!"}



@router.post("/register")
def register(username: str, password: str, db = Depends(get_db)):

    # check if user exists
    cursor = db.execute(
        "SELECT * FROM users WHERE email = ?",
        (username,)
    )
    user = cursor.fetchone()

    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    # insert new user
    db.execute(
        "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
        (username, username, hash_password(password), "student")
    )

    return {"message": "User created successfully"}


@router.post("/login")
def login(username: str, password: str, db = Depends(get_db)):

    cursor = db.execute(
        "SELECT * FROM users WHERE email = ?",
        (username,)
    )
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # user = (id, name, email, password, role)
    stored_password = user[3]

    if not verify_password(password, stored_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")


    token = create_access_token({'role': 'user', 'user_name': user[1]})

    return {"token": token}