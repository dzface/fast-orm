#validation.py
from pydantic import BaseModel

class UserBase(BaseModel):
  user_id: str
  user_name: str
  password: str
class PostBase(BaseModel):
  title: str
  content: str
  user_id: int

