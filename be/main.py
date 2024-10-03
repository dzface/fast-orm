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
#Base.metadata.drop_all(bind=engine)  # 모든 테이블 삭제
Base.metadata.create_all(bind=engine)  # 테이블 생성
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def main():
  return {"Hello FastAPI!"}

#유저 생성
@app.post("/user/sign-up", status_code=status.HTTP_201_CREATED)
async def create_user(user: validation.UserBase, db:db_dependency):
  db_user = model.User(**user.dict())
  db.add(db_user)
  db.commit()

#유저 id로 정보조회
@app.post("/user/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: str, db: db_dependency):
  user = db.query(model.User).filter(model.User.user_id == user_id).first()
  if user is None:
    raise HTTPException(status_code=404, detail='User not found')
  return user

#유저 정보 수정
@app.put("/user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(user_id: str, user_update: validation.UserBase, db: db_dependency):
  # user_id에 해당하는 유저를 DB에서 검색
  user = db.query(model.User).filter(model.User.user_id == user_id).first()

  # 유저가 존재하지 않을 경우 예외 발생
  if user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  # 유저 정보 업데이트
  user.user_id = user_update.user_id
  user.user_name = user_update.user_name
  user.password = user_update.password

  # 데이터베이스에 변경 사항 반영
  db.commit()
  db.refresh(user)

  return {"message": "User updated successfully", "user": user}

#유저 삭제
@app.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id:str, db: db_dependency):
  user = db.query(model.User).filter(model.User.user_id == user_id).first()
  if user is None:
    raise HTTPException(status_code=404, detail='User was not found')
  db.delete(user)
  db.commit()