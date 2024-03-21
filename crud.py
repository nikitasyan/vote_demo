import models
from sqlalchemy.orm import Session


def vote_for_option_by_id(db: Session, option_id: int):
    option = db.get(models.Option, option_id)
    option.vote_count += 1
    db.commit()
    db.refresh(option)
    return option


def create_vote(db: Session, text_question: str):
    new_question = models.Question(text_question=text_question)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question


def create_options(db: Session, options: list[str], question_id: int):
    for opt in options:
        option = models.Option(answer=opt, question_id=question_id)
        db.add(option)
    db.commit()
    new_options = db.query(models.Option).filter(models.Option.question_id == question_id).all()
    return new_options


def get_all_votes(db: Session):
    return db.query(models.Question).all()


def get_all_options(db: Session):
    return db.query(models.Option).all()


def get_vote_by_id(db: Session, question_id: int):
    return db.get(models.Question, question_id)


def get_option_by_id(db: Session, option_id: int):
    return db.get(models.Option, option_id)


def get_vote_by_text_question(db: Session, text_question: str):
    return db.query(models.Question).filter(models.Question.text_question == text_question).first()


def delete_vote_by_id(db: Session, question_id: int):
    current_question = db.get(models.Question, question_id)
    db.delete(current_question)
    db.commit()
    return "Successful deleted"
