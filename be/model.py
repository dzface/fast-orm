#model.py
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key=True, index=True)
  custom_id = Column(String(50), unique=True)
  user_name = Column(String(50))
  password = Column(String(100))

  # Post와의 관계 정의 (1:N)
  posts = relationship("Post", back_populates="user")

class Post(Base):
  __tablename__ = 'post'
  id = Column(Integer, primary_key=True, index=True)
  title = Column(String(50))
  content = Column(String(100))
  custom_id=Column(String(50), ForeignKey('user.custom_id'))

  # User와의 관계 정의
  user = relationship("User", back_populates="posts")