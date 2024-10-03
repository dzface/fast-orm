#validation.py
from pydantic import BaseModel

class UserBase(BaseModel):
  custom_id: str
  user_name: str
  password: str

class PostBase(BaseModel):
  custom_id: str
  title: str
  content: str

