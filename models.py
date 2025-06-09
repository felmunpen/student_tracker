from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base

from enum import Enum
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=True)


# class BlocksValues(str, Enum):
#     operaciones = "Operaciones"
#     algebra = "Álgebra"
#     geometria = "Geometría"
#     estadistica = "Estadística y probabilidad"
#     funciones = "Funciones"


class Block(Base):
    __tablename__ = "blocks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # __table_args__ = (
    #     CheckConstraint("valor IN ('Operaciones', 'Álgebra', 'Geometría', 'Estadística y probabilidad', 'Funciones')",
    #                     name="check_valores_permitidos"),
    # )


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    block_id = Column(Float, ForeignKey("blocks.id"), nullable=True)
    grade = Column(Float, nullable=True)
    course = Column(String, nullable=False)
    classroom = Column(String, nullable=False)
    year = Column(String, nullable=False)

