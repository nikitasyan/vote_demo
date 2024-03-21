from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException, Depends

from database import SessionLocal, Base, engine
from schemas import Option, Question, QuestionBase, OptionBase
import crud


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/vote/{option_id}", response_model=Option)
def vote_for_option_by_id(option_id: int, db: Session = Depends(get_db)):
    option = crud.get_option_by_id(db, option_id)
    if option:
        return crud.vote_for_option_by_id(db, option_id)
    raise HTTPException(status_code=404, detail="Incorrect value option")


@app.post("/create/vote", response_model=QuestionBase)
def create_vote(text_question: str, db: Session = Depends(get_db)):
    vote = crud.get_vote_by_text_question(db, text_question)
    if vote:
        raise HTTPException(status_code=400, detail="This question already exist")
    return crud.create_vote(db, text_question)


@app.post("/create/options", response_model=list[Option])
def create_options(options: list[str], question_id: int, db: Session = Depends(get_db)):
    question = crud.get_vote_by_id(db, question_id)
    if question:
        return crud.create_options(db, options, question_id)
    raise HTTPException(status_code=404, detail="This question not found")


@app.get("/all_votes/", response_model=list[Question])
def get_all_votes(db: Session = Depends(get_db)):
    return crud.get_all_votes(db)


@app.get("/app_questions/", response_model=list[QuestionBase])
def get_all_questions(db: Session = Depends(get_db)):
    return crud.get_all_votes(db)


@app.get("/all_options/", response_model=list[OptionBase])
def get_all_options(db: Session = Depends(get_db)):
    return crud.get_all_options(db)


@app.get("/result_vote/{question_id}", response_model=Question)
def get_vote_by_id(question_id: int, db: Session = Depends(get_db)):
    vote = crud.get_vote_by_id(db, question_id)
    if vote:
        return vote
    raise HTTPException(status_code=404, detail="Vote not found")


@app.delete("/delete_vote/{question_id}", response_model=str)
def delete_vote_by_id(question_id: int, db: Session = Depends(get_db)):
    vote = crud.get_vote_by_id(db, question_id)
    if vote:
        return crud.delete_vote_by_id(db, question_id)
    raise HTTPException(status_code=400, detail="Incorrect input data. Object not found")
