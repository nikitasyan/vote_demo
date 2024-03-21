from pydantic import BaseModel


class OptionBase(BaseModel):
    answer: str
    vote_count: int


class Option(OptionBase):
    id: int
    question_id: int


class QuestionBase(BaseModel):
    text_question: str


class Question(QuestionBase):
    id: int
    options: list[Option] = []
