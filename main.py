# 文件: main.py
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from sqlmodel import SQLModel, Session, select
from contextlib import asynccontextmanager
from typing import List, Optional
import os
import uuid
from models import Survey, Response
from schemas import SurveyRead, ResponseRead
from schemas import SurveyCreate, ResponseCreate
from crud import create_survey, get_survey_by_id, get_all_surveys, get_survey_ids, create_response, get_response_by_id, get_responses_by_survey_id, get_all_responses
from database import engine, get_session
from config import UPLOAD_DIR

# 确保上传目录存在
os.makedirs(UPLOAD_DIR, exist_ok=True)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    print("Application starting up...")
    # 确保数据库表存在
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)
    print("Database tables checked/created.")
    yield
    # shutdown
    print("Application shutting down...")

app = FastAPI(lifespan=lifespan)

# --- Survey Routes ---
@app.post("/surveys/", response_model=SurveyRead)
def create_survey_endpoint(survey: SurveyCreate, db: Session = Depends(get_session)):
    db_survey = create_survey(db, survey)
    return db_survey

@app.get("/surveys/{survey_id}", response_model=SurveyRead)
def read_survey(survey_id: uuid.UUID, db: Session = Depends(get_session)):  # 修改為 uuid.UUID
    db_survey = get_survey_by_id(db, survey_id)
    if not db_survey:
        raise HTTPException(status_code=404, detail="Survey not found")
    return db_survey

@app.get("/surveys/", response_model=List[SurveyRead])
def read_all_surveys(db: Session = Depends(get_session)):
    surveys = get_all_surveys(db)
    return surveys

# --- Response Routes ---
@app.post("/responses/", response_model=ResponseRead)
def create_new_response(
    survey_id: uuid.UUID,
    employee_name: str = Form(...),
    text_response: str = Form(None),
    file: UploadFile = File(None), # 允许文件上传
    db: Session = Depends(get_session)
):
    # 检查 Survey ID 是否存在
    survey = get_survey_by_id(db, survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    file_path = None
    if file:
        # 生成唯一文件名
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{survey_id}_{employee_name}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        # 保存文件
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

    # 创建 Response 对象，包含文件路径
    response_obj = ResponseCreate(
        survey_id=survey_id,
        employee_name=employee_name,
        text_response=text_response,
        file_response_path=file_path # 如果没有上传文件，这里会是 None
    )

    db_response = create_response(db, response_obj)
    return db_response

@app.get("/responses/{response_id}", response_model=ResponseRead)
def read_response(response_id: uuid.UUID, db: Session = Depends(get_session)):  # 修改為 uuid.UUID
    db_response = get_response_by_id(db, response_id)
    if not db_response:
        raise HTTPException(status_code=404, detail="Response not found")
    return db_response

@app.get("/responses/survey/{survey_id}", response_model=List[ResponseRead])
def read_responses_for_survey(survey_id: uuid.UUID, db: Session = Depends(get_session)):  # 修改為 uuid.UUID
    responses = get_responses_by_survey_id(db, survey_id)
    return responses

@app.get("/responses/", response_model=List[ResponseRead])
def read_all_responses(db: Session = Depends(get_session)):
    responses = get_all_responses(db)
    return responses

# --- Debug/Utility Route ---
@app.get("/survey-ids/")
def get_survey_ids_list(db: Session = Depends(get_session)):
    # 修正：使用修正后的函数
    ids = get_survey_ids(db)
    return {"survey_ids": ids}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)