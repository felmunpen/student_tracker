from pydantic import BaseModel
from typing import Optional


class StudentBase(BaseModel):
    name: str
    gender: Optional[str] = None


class StudentCreate(StudentBase):
    pass


class Student(StudentBase):
    id: int

    class Config:
        orm_mode = True

#


class BlockBase(BaseModel):
    name: str


class BlockCreate(BlockBase):
    pass


class Block(BlockBase):
    id: int

    class Config:
        orm_mode = True
#


class GradeBase(BaseModel):
    student_id: int
    block_id: int
    grade: Optional[float] = None
    course: int
    classroom: str
    year: str


class GradeCreate(GradeBase):
    pass


class Grade(GradeBase):
    id: int

    class Config:
        orm_mode = True

class ChatInput(BaseModel):
    message: str

