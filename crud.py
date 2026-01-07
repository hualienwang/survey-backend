# 文件: crud.py
from sqlmodel import Session, select
from models import Survey, Response, SurveyCreate, ResponseCreate
from typing import List

def create_survey(db: Session, survey: SurveyCreate) -> Survey:
    db_survey = Survey.from_orm(survey) if hasattr(survey, 'dict') else Survey(**survey.dict()) # 兼容 pydantic v1/v2
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    return db_survey

def get_survey_by_id(db: Session, survey_id: int) -> Survey:
    return db.get(Survey, survey_id)

def get_all_surveys(db: Session) -> List[Survey]:
    return db.exec(select(Survey)).all()

def get_survey_ids(db: Session) -> List[int]: # 修正：直接返回 id 列表
    # select(Survey.id) 返回的就是 id 值本身，不需要再访问 .id
    return [survey_id for survey_id in db.exec(select(Survey.id)).all()]

def create_response(db: Session, response: ResponseCreate) -> Response:
    db_response = Response.from_orm(response) if hasattr(response, 'dict') else Response(**response.dict()) # 兼容 pydantic v1/v2
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def get_response_by_id(db: Session, response_id: int) -> Response:
    return db.get(Response, response_id)

def get_responses_by_survey_id(db: Session, survey_id: int) -> List[Response]:
    return db.exec(select(Response).where(Response.survey_id == survey_id)).all()

def get_all_responses(db: Session) -> List[Response]:
    return db.exec(select(Response)).all()