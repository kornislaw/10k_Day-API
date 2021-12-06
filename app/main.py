from typing import Optional

import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


try:
    # this is for psycopg v3:
    # conn = psycopg.connect(
    #     "host=localhost dbname=10kday user=postgres password=postgres"
    # )
    # cursor = conn.cursor(row_factory=psycopg.rows.dict_row)

    conn = psycopg2.connect(
        host="localhost",
        database="10kday",
        user="postgres",
        password="postgres",
        cursor_factory=RealDictCursor,
    )
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connection to the DB has failed")
    print(f"Error: {error}")


def find_exercise(exe_id):
    cursor.execute("""SELECT * FROM exercises WHERE id=%s""", (exe_id,))
    return cursor.fetchone()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/exercises")
async def get_exercises(db: Session = Depends(get_db)):
    execs = db.query(models.Exercise).all()
    return execs


@app.get("/exercises/{id}")
async def get_exercise(id: int, db: Session = Depends(get_db)):
    # exe = find_exercise(id)
    exe = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not exe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return exe


@app.post("/exercise", status_code=status.HTTP_201_CREATED)
async def post_exercise(exercise: schemas.Exercise, db: Session = Depends(get_db)):
    new_exe = models.Exercise(**exercise.dict())
    db.add(new_exe)
    db.commit()
    db.refresh(new_exe)
    return new_exe


@app.put("/exercises/{id}")
async def update_exercise(id: int, exe: schemas.Exercise, db: Session = Depends(get_db)):
    up_exe_query = db.query(models.Exercise).filter(models.Exercise.id == id)
    up_exe = up_exe_query.first()
    if up_exe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise ID {id} does not exist",
        )
    up_exe_query.update(exe.dict(), synchronize_session=False)
    db.commit()
    return up_exe_query.first()


@app.delete("/exercises/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    exe = db.query(models.Exercise).filter(models.Exercise.id == id)

    if exe.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise ID {id} does not exist",
        )
    exe.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# /exercises
# /repeats {exercise_id}
# /sequences
# /workouts
# /workout-items {foreign keys: exercise_id, repeat_id, workout_id, user_id}
# /users
