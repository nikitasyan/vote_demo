from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    text_question = Column(String(100), nullable=False, unique=True)

    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True)
    answer = Column(String(50), nullable=False, unique=True)
    vote_count = Column(Integer, default=0)
    question_id = Column(Integer, ForeignKey("questions.id"))

    question = relationship("Question", back_populates="options")
