from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# ───── ГРУППЫ ─────

class GroupBase(BaseModel):
    name: str = Field(..., example="ИС-22-1")

class GroupOut(GroupBase):
    id: int
    class Config:
        orm_mode = True

# ───── ПОЛЬЗОВАТЕЛИ ─────

class AnswerSubmit(BaseModel):
    question_id: int
    response: str

class SurveySubmit(BaseModel):
    survey_id: int
    answers: List[AnswerSubmit]

class SubmitSurvey(BaseModel):
    survey_id: int
    answers: List[AnswerSubmit]

class UserCreate(BaseModel):
    username: str = Field(..., example="ivanov01")
    password: str = Field(..., example="qwerty123")
    full_name: Optional[str] = Field(None, example="Иванов Иван")
    role: str = Field(..., example="student")  # student / teacher
    group_id: Optional[int] = Field(None, example=1)  # только для студентов

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    full_name: Optional[str]
    role: str
    group: Optional[GroupOut]

    class Config:
        orm_mode = True

# ───── АНКЕТЫ ─────

class QuestionOptionCreate(BaseModel):
    text: str

class QuestionCreate(BaseModel):
    text: str
    type: str  # open / closed / semi-closed
    options: Optional[List[QuestionOptionCreate]] = None  # для closed / semi-closed

class SurveyCreate(BaseModel):
    title: str
    anonymous: bool = True
    start_date: datetime
    end_date: datetime
    group_id: Optional[int]
    questions: List[QuestionCreate]


# ───── ВЫВОД АНКЕТЫ ─────
class QuestionOptionOut(BaseModel):
    id: int
    text: str

    class Config:
        orm_mode = True

# ───── ВЫВОД ВОПРОСА ─────

class QuestionOut(BaseModel):
    id: int
    text: str
    type: str
    options: List[QuestionOptionOut] = []  # <== обязательно

    class Config:
        orm_mode = True

class SurveyOut(BaseModel):
            id: int
            title: str
            anonymous: bool
            start_date: datetime
            end_date: datetime
            group_id: int
            creator_id: int
            questions: List[QuestionOut] = []

            class Config:
                orm_mode = True
