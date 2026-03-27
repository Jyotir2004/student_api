from pydantic import BaseModel

class UserRegister(BaseModel):
    name: str
    email: str
    password: str
    role: str  # student / teacher / admin


class UserLogin(BaseModel):
    name: str
    password: str