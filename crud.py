# 文件: crud.py
from sqlmodel import Session, select
from models import Survey, Response
from schemas import SurveyCreate, ResponseCreate
from typing import List
import uuid

def create_survey(db: Session, survey: SurveyCreate) -> Survey:
    db_survey = Survey.model_validate(survey) if hasattr(Survey, 'model_validate') else Survey(**survey.model_dump()) # 兼容 pydantic v2
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey

def get_survey_by_id(db: Session, survey_id: uuid.UUID) -> Survey:
    return db.get(Survey, survey_id)

def get_all_surveys(db: Session) -> List[Survey]:
    return db.exec(select(Survey)).all()

def get_survey_ids(db: Session) -> List[uuid.UUID]:
    survey_ids = db.exec(select(Survey.id)).all()
    return [item for item in survey_ids]

def create_response(db: Session, response: ResponseCreate) -> Response:
    db_response = Response.model_validate(response) if hasattr(Response, 'model_validate') else Response(**response.model_dump()) # 兼容 pydantic v2
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def get_response_by_id(db: Session, response_id: uuid.UUID) -> Response:
    return db.get(Response, response_id)

def get_responses_by_survey_id(db: Session, survey_id: uuid.UUID) -> List[Response]:
    return db.exec(select(Response).where(Response.survey_id == survey_id)).all()

def get_all_responses(db: Session) -> List[Response]:
    return db.exec(select(Response)).all()