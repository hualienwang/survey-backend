# backend/schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

# Survey Schemas
class SurveyBase(BaseModel):
    title: str
    description: Optional[str] = None

class SurveyCreate(SurveyBase):
    pass

class SurveyRead(SurveyBase):
    id: uuid.UUID
    created_at: datetime

# Response Schemas
class ResponseBase(BaseModel):
    survey_id: uuid.UUID
    employee_name: str
    text_response: Optional[str] = None

class ResponseCreate(ResponseBase):
    file_response_path: Optional[str] = None

class ResponseRead(ResponseBase):
    id: uuid.UUID
    file_response_path: Optional[str] = None # 可选，因为可能没有文件
    submitted_at: datetime