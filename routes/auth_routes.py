from fastapi import APIRouter, Depends, HTTPException
from api import Database, get_db
from auth import hash_password, verify_password, create_access_token
from models import UserRegister, UserLogin

router = APIRouter()


@router.post("/register")
def register(user: UserRegister, db: Database = Depends(get_db)):
    hashed_password = hash_password(user.password)

    # Check if user already exists
    existing = db.execute(
        "SELECT id FROM users WHERE name=? OR email=?",
        (user.name, user.email)
    ).fetchone()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    db.execute(
        "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
        (user.name, user.email, hashed_password, user.role)
    )

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin, db: Database = Depends(get_db)):
    result = db.execute(
        "SELECT name, password, role FROM users WHERE name=?",
        (user.name,)
    )

    db_user = result.fetchone()

    
    if not db_user or not verify_password(user.password, db_user[1]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    
    token = create_access_token({
        "sub": db_user[0],   
        "role": db_user[2]
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }