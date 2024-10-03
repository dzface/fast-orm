#main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated


# config.py에서 Base와 engine 가져오기
from config import get_db, Base, engine
import model
import validation

app = FastAPI()
# 테이블을 삭제한 후 다시 생성하는 코드
Base.metadata.drop_all(bind=engine)  # 모든 테이블 삭제
Base.metadata.create_all(bind=engine)  # 테이블 다시 생성
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def main():
  return {"Hello FastAPI!"}

#유저 생성
@app.post("/user/sign-up")
async def create_user(user: validation.UserBase, db:db_dependency):
  db_user = model.User(**user.dict())
  db.add(db_user)
  db.commit()
