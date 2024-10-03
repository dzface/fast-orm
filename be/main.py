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
##Base.metadata.drop_all(bind=engine)  # 모든 테이블 삭제
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
@app.post("/user/{custom_id}", status_code=status.HTTP_200_OK)
async def read_user(custom_id: str, db: db_dependency):
  user = db.query(model.User).filter(model.User.custom_id == custom_id).first()
  if user is None:
    raise HTTPException(status_code=404, detail='User not found')
  return user

#유저 정보 수정
@app.put("/user/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(custom_id: str, user_update: validation.UserBase, db: db_dependency):
  # custom_id에 해당하는 유저를 DB에서 검색
  user = db.query(model.User).filter(model.User.custom_id == custom_id).first()

  # 유저가 존재하지 않을 경우 예외 발생
  if user is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  # 유저 정보 업데이트
  user.custom_id = user_update.custom_id
  user.user_name = user_update.user_name
  user.password = user_update.password

  # 데이터베이스에 변경 사항 반영
  db.commit()
  db.refresh(user)

  return {"message": "User updated successfully", "user": user}

#유저 삭제
@app.delete("/user/{custom_id}", status_code=status.HTTP_200_OK)
async def delete_user(custom_id:str, db: db_dependency):
  user = db.query(model.User).filter(model.User.custom_id == custom_id).first()
  if user is None:
    raise HTTPException(status_code=404, detail='User was not found')
  db.delete(user)
  db.commit()

# 게시글 작성
@app.post("/post", status_code=status.HTTP_201_CREATED)
async def create_post(post: validation.PostBase, db: db_dependency):
  db_post = model.Post(**post.dict())
  db.add(db_post)
  db.commit()

# 모든게시글 조회
@app.get("/post", status_code=status.HTTP_200_OK)
async def read_user_posts(db: db_dependency):
  posts = db.query(model.Post).all()
  return posts

#유저 아이디로 게시글 조회
@app.get("/post/{custom_id}", status_code=status.HTTP_200_OK)
async def read_user_posts(custom_id:str, db: db_dependency):
  user_posts = db.query(model.Post).filter(model.Post.custom_id == custom_id).all()
  return user_posts

#게시글 아이디 경로 변수로 받아서 게시글수정
@app.put("/post/{post_id}", status_code=status.HTTP_200_OK)
async def update_post(custom_id: str, post_id: int, post_update: validation.PostBase, db: db_dependency):
  # custom_id에 해당하는 유저를 DB에서 검색
  user = db.query(model.User).filter(model.User.custom_id == custom_id).first()
  # 유저가 존재하지 않을 경우 예외 발생
  if user.custom_id is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  # post_id에 해당하는 게시글을 DB에서 검색
  post = db.query(model.Post).filter(model.Post.id == post_id).first()
  # 게시글이 존재하지 않을 경우 예외 발생
  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
  # 게시글 작성자가 해당 유저인지 확인
  if post.custom_id != user.custom_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized to update this post")
  # 게시글 정보 업데이트
  post.title = post_update.title
  post.content = post_update.content
  # 데이터베이스에 변경 사항 반영
  db.commit()
  db.refresh(post)

  return {"message": "Post updated successfully"}

# 게시글 아이디 경로 변수로 받아서 게시글 삭제
@app.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(custom_id: str, post_id: int, db: db_dependency):
  # custom_id에 해당하는 유저를 DB에서 검색
  user = db.query(model.User).filter(model.User.custom_id == custom_id).first()
  # 유저가 존재하지 않을 경우 예외 발생
  if user is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

  # post_id에 해당하는 게시글을 DB에서 검색
  post = db.query(model.Post).filter(model.Post.id == post_id).first()
  # 게시글이 존재하지 않을 경우 예외 발생
  if post is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

  # 게시글 작성자가 해당 유저인지 확인
  if post.custom_id != user.custom_id:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User is not authorized to delete this post")

  # 게시글 삭제
  db.delete(post)
  db.commit()

  return {"message": "Post deleted successfully"}
