#config.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


URL_DATABASE = 'mysql+pymysql://admin:1234@localhost:3306/fast-orm'
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind=engine)
Base = declarative_base()

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

