from sqlalchemy import Column, Integer, String
# from src.utils.database import Base

class User():
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)