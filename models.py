# backend/models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid

# Survey 表
class SurveyBase(SQLModel):
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Survey(SurveyBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # 一个调查可以有多个回应
    responses: List["Response"] = Relationship(back_populates="survey")

# Response 表
class ResponseBase(SQLModel):
    survey_id: uuid.UUID = Field(foreign_key="survey.id")
    employee_name: str = Field(index=True)
    text_response: Optional[str] = Field(default=None)
    file_response_path: Optional[str] = Field(default=None) # 存储文件在服务器上的路径
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

class Response(ResponseBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    # 一个回应对应一个调查
    survey: Survey = Relationship(back_populates="responses")