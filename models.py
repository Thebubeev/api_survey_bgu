from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class StudentGroup(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    students = relationship("User", back_populates="group")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String)
    role = Column(String)  # student / teacher

    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    group = relationship("StudentGroup", back_populates="students")

    surveys = relationship("Survey", back_populates="creator")
    answers = relationship("Answer", back_populates="user")
    notifications = relationship("Notification", back_populates="user")


class Survey(Base):
    __tablename__ = "surveys"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    anonymous = Column(Boolean, default=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    creator_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)

    creator = relationship("User", back_populates="surveys")
    group = relationship("StudentGroup")
    questions = relationship("Question", back_populates="survey", cascade="all, delete")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    type = Column(String, nullable=False)  # open / closed / semi-closed
    survey_id = Column(Integer, ForeignKey("surveys.id"))

    survey = relationship("Survey", back_populates="questions")
    answers = relationship("Answer", back_populates="question")
    options = relationship("QuestionOption", back_populates="question", cascade="all, delete")


class QuestionOption(Base):
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"))

    question = relationship("Question", back_populates="options")


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    response = Column(Text, nullable=True)  # текст ответа для open-вопросов
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # null если anonymous=True

    question = relationship("Question", back_populates="answers")
    user = relationship("User", back_populates="answers")


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="notifications")
