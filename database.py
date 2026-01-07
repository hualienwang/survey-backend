# backend/database.py
from sqlmodel import create_engine, Session
import os
# from config import DATABASE_URL, UPLOAD_DIR
# 使用 SQLite 数据库
# DATABASE_URL = "sqlite:///./survey.db"
DATABASE_URL = f"postgresql://postgres:1234@localhost:5432/surveydb"
# 创建数据库引擎
engine = create_engine(DATABASE_URL, echo=True) # echo=True 用于调试，显示 SQL 语句

def get_session():
    with Session(engine) as session:
        yield session