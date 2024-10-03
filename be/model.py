#model.py
from sqlalchemy import Column, String, Integer
from config import Base

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(String(50), unique=True)
  user_name = Column(String(50))
  password = Column(String(100))

class Post(Base):
  __tablename__ = 'post'
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(50))
  content = Column(String(100))
  user_id=Column(Integer)