# backend/database.py
from sqlmodel import create_engine, Session
from config import DATABASE_URL

# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True) # echo=True 用于调试，显示 SQL 语句

def get_session():
    with Session(engine) as session:
        yield session