from cgitb import text
from collections import defaultdict
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
import models
import schemas
from database import SessionLocal, engine, Base
from sqlalchemy.sql import func
import openai

##############
from pydantic import BaseModel
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_community.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

###########
# Conecta a la base SQLite
db = SQLDatabase.from_uri("sqlite:///db.sqlite3")

# Usa GPT-4o como modelo base
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
llm = ChatOpenAI(temperature=0, model="gpt-4o")

# Crea el toolkit con la BD
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# Crea el agente
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True  # Muestra pasos intermedios por consola
)

# Consulta en lenguaje natural
# agent_executor.run("¿Cuál es la nota media de los alumnos?")

###########
app = FastAPI()

#
app.add_middleware(
    CORSMiddleware,
    # Cambia esto a ["http://localhost:3000"] en producción
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear tablas en la BD
Base.metadata.create_all(bind=engine)

# Dependencia para obtener sesión de BD


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints para Alumno


@app.post("/students", response_model=schemas.Student)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=list[schemas.Student])
def show_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@app.get("/students/{student_id}", response_model=schemas.Student)
def show_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Blocks
@app.get("/blocks", response_model=list[schemas.Block])
def show_blocks(db: Session = Depends(get_db)):
    return db.query(models.Block).all()


# Endpoints para Calificacion
@app.post("/grades", response_model=schemas.Grade)
def create_grade(grade: schemas.GradeCreate, db: Session = Depends(get_db)):
    if not db.query(models.Student).filter(models.Student.id == grade.student_id).first():
        raise HTTPException(status_code=404, detail="Student not found")
    if not db.query(models.Black).filter(models.Block.id == grade.block_id).first():
        raise HTTPException(status_code=404, detail="Block not found")
    db_grade = models.Grade(**grade.dict())
    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)
    return db_grade


@app.get("/grades", response_model=list[schemas.Grade])
def show_grades(db: Session = Depends(get_db)):
    return db.query(models.Grade).all()


@app.get("/grades-by-user")
def show_grades_by_user(db: Session = Depends(get_db)):

    query = text(
        "SELECT student_id, GROUP_CONCAT(grade) AS grades_group FROM grades GROUP BY student_id")
    result = db.execute(query)
    res = result.fetchall()
    results = {}
    for student_id, grades_group in res:
        results[student_id] = [grades_group]

    return results


@app.get("/avg-block-grade")
def avg_block_grade(db: Session = Depends(get_db)):

    query = text(
        "SELECT block_id, AVG(grade) FROM grades GROUP BY block_id")
    result = db.execute(query)
    res = result.fetchall()
    results = {}
    for block_id, block_avg in res:
        results[str(int(block_id))] = [round(block_avg, 2)]

    return results

@app.get("/avg-student-grade")
def avg_student_grade(db: Session = Depends(get_db)):

    query = text(
        "SELECT student_id, AVG(grade) FROM grades GROUP BY student_id")
    result = db.execute(query)
    res = result.fetchall()
    results = {}
    for student_id, grade_avg in res:
        results[str(int(student_id))] = [round(grade_avg, 2)]

    return results


######################

def chat_with_gpt(prompt):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    while True:
        user_input = input ("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot: ", response)


@app.post("/chat")
def chat(input: schemas.ChatInput):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input.message}]
    )
    return {"response": response.choices[0].message.content.strip()}


@app.post("/chatbot")
def chat(input: schemas.ChatInput):
    try:
        respuesta = agent_executor.run(input.message)
        return {"response": respuesta}
    except Exception as e:
        return {"error": str(e)}