from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from auth import create_access_token, get_current_user
from database import engine, SessionLocal, get_db
from models import Base, User, StudentGroup, Survey, Question, QuestionOption, Answer
from schemas import (
    UserCreate, UserLogin, UserOut,
    GroupBase, GroupOut,
    SurveyCreate, QuestionCreate, QuestionOptionCreate,
    QuestionOut, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate,
    SurveyCreate, SurveyCreate, SurveyCreate, SurveyCreate, SubmitSurvey, SurveyOut, SurveySubmit
)
from datetime import datetime
from typing import List
import hashlib

# Инициализация FastAPI
app = FastAPI()

# Создание таблиц
Base.metadata.create_all(bind=engine)



# Хеширование пароля
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ───── РЕГИСТРАЦИЯ ─────
@app.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    if user.role == "student":
        group = db.query(StudentGroup).filter(StudentGroup.id == user.group_id).first()
        if not group:
            raise HTTPException(status_code=400, detail="Группа не найдена")

    new_user = User(
        username=user.username,
        password_hash=hash_password(user.password),
        full_name=user.full_name,
        role=user.role,
        group_id=user.group_id if user.role == "student" else None
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ───── ЛОГИН ─────
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    hashed = hash_password(form_data.password)
    db_user = db.query(User).filter(User.username == form_data.username, User.password_hash == hashed).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# ───── СОЗДАНИЕ ГРУППЫ ─────
@app.post("/groups/", response_model=GroupOut)
def create_group(group: GroupBase, db: Session = Depends(get_db)):
    if db.query(StudentGroup).filter(StudentGroup.name == group.name).first():
        raise HTTPException(status_code=400, detail="Группа уже существует")
    new_group = StudentGroup(name=group.name)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

@app.get("/user")
def get_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return current_user
# ───── СОЗДАНИЕ АНКЕТЫ ─────
@app.post("/surveys/")
def create_survey(
    survey: SurveyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Только для преподавателей")

    new_survey = Survey(
        title=survey.title,
        anonymous=survey.anonymous,
        start_date=survey.start_date,
        end_date=survey.end_date,
        creator_id=current_user.id,
        group_id=survey.group_id
    )
    db.add(new_survey)
    db.flush()  # Получить new_survey.id

    for q in survey.questions:
        new_q = Question(
            text=q.text,
            type=q.type,
            survey_id=new_survey.id
        )
        db.add(new_q)
        db.flush()  # Получить new_q.id

        if q.options:
            for opt in q.options:
                new_opt = QuestionOption(
                    text=opt.text,
                    question_id=new_q.id
                )
                db.add(new_opt)

    db.commit()  # Коммит после добавления всех
    return {"message": "Анкета создана"}


# ───── ПОЛУЧЕНИЕ ДОСТУПНЫХ АНКЕТ ─────
@app.get("/surveys/students/available")
def get_available_surveys(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    now = datetime.utcnow()

    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Только для студентов")

    surveys = db.query(Survey).filter(

        (Survey.group_id == None) | (Survey.group_id == current_user.group_id)
    ).all()

    return surveys

@app.get("/surveys/submitted")
def get_submitted_surveys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Только для преподавателей")

    # Получаем все анкеты, созданные преподавателем
    surveys = db.query(Survey).filter(Survey.creator_id == current_user.id).all()

    result = []
    for survey in surveys:
        survey_answers = []

        for question in survey.questions:
            answers = db.query(Answer).filter(Answer.question_id == question.id).all()

            if answers:
                survey_answers.append({
                    "question_id": question.id,
                    "text": question.text,
                    "answers": [
                        {"answer_id": a.id, "response": a.response, "user_id": a.user_id} for a in answers
                    ]
                })

        # Добавлять только те анкеты, у которых есть хотя бы один ответ
        if survey_answers:
            result.append({
                "survey_id": survey.id,
                "title": survey.title,
                "answers": survey_answers
            })

    return result

@app.get("/surveys/teachers/available")
def get_created_surveys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Только для преподавателей")

    surveys = db.query(Survey).filter(Survey.creator_id == current_user.id).all()
    return surveys

@app.post("/surveys/submit")
def submit_survey(data: SurveySubmit, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Проверка: только студент
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Только для студентов")

    survey = db.query(Survey).filter(Survey.id == data.survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Анкета не найдена")

    for ans in data.answers:
        question = db.query(Question).filter(Question.id == ans.question_id, Question.survey_id == survey.id).first()
        if not question:
            raise HTTPException(status_code=404, detail=f"Вопрос с id={ans.question_id} не найден в анкете")

        answer = Answer(
            response=ans.response,
            question_id=ans.question_id,
            user_id=None if survey.anonymous else current_user.id
        )
        db.add(answer)

    db.commit()
    return {"message": "Ответы успешно сохранены"}


@app.get("/surveys/{survey_id}", response_model=SurveyOut)
def get_survey(survey_id: int, db: Session = Depends(get_db)):
    survey = db.query(Survey).options(
        joinedload(Survey.questions)
        .joinedload(Question.options)
    ).filter(Survey.id == survey_id).first()

    if not survey:
        raise HTTPException(status_code=404, detail="Анкета не найдена")

    return survey

from sqlalchemy.orm import joinedload


