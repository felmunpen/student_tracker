import sqlite3
import random
import string

# Crear conexión y cursor
# conn = sqlite3.connect("escuela.db")
conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Crear tablas
# cursor.executescript("""
# DROP TABLE IF EXISTS calificaciones;
# DROP TABLE IF EXISTS alumnos;
# DROP TABLE IF EXISTS bloques;

# CREATE TABLE alumnos (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nombre TEXT NOT NULL,
#     sexo TEXT CHECK(sexo IN ('M', 'F')) NOT NULL
# );

# CREATE TABLE bloques (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nombre TEXT NOT NULL
# );

# CREATE TABLE calificaciones (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_alumno INTEGER NOT NULL,
#     id_bloque INTEGER NOT NULL,
#     nota REAL NOT NULL,
#     clase TEXT NOT NULL DEFAULT 'a',
#     curso INTEGER NOT NULL DEFAULT 2024,
#     FOREIGN KEY(id_alumno) REFERENCES alumnos(id),
#     FOREIGN KEY(id_bloque) REFERENCES bloques(id)
# );
# """)

# Insertar bloques
blocks_names = ["Arithmetic", "Algebra", "Geometry",
                "Probability", "Functions"]
cursor.executemany("INSERT INTO blocks (name) VALUES (?)", [
                   (name,) for name in blocks_names])

# Generar nombres aleatorios (sencillos para esta práctica)


def generate_name():
    return ''.join(random.choices(string.ascii_uppercase, k=1)) + ''.join(random.choices(string.ascii_lowercase, k=6))


# Insertar alumnos
students = []
for _ in range(30):
    name = generate_name()
    gender = random.choice(['M', 'F'])
    students.append((name, gender))
cursor.executemany(
    "INSERT INTO students (name, gender) VALUES (?, ?)", students)

# Obtener IDs
cursor.execute("SELECT id FROM students")
students_id = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM blocks")
blocks_id = [row[0] for row in cursor.fetchall()]

# Insertar calificaciones realistas
grades = []
for student_id in students_id:
    type = random.choices(['good', 'standard', 'bad'],
                          weights=[0.3, 0.4, 0.3])[0]

    if type == 'good':
        base = random.uniform(7.5, 9.5)
    elif type == 'standard':
        base = random.uniform(5.0, 7.0)
    else:  # bad
        base = random.uniform(2.5, 4.5)

    for block_id in blocks_id:
        grade = round(random.gauss(base, 0.5), 1)
        grade = max(0, min(10, grade))  # Asegurar rango 0-10
        grades.append((student_id, block_id, grade, '4', 'a', 2024))

cursor.executemany("""
    INSERT INTO grades (student_id, block_id, grade, course, classroom, year)
    VALUES (?, ?, ?, ?, ?, ?)
""", grades)

conn.commit()
conn.close()

print("Database created and populated successfully.")
