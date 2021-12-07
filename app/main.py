from typing import Optional, List

import psycopg2
from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
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


@app.get("/exercises", response_model=List[schemas.Exercise])
async def get_exercises(db: Session = Depends(get_db)):
    execs = db.query(models.Exercise).all()
    return execs


@app.get("/exercises/{id}", response_model=schemas.Exercise)
async def get_exercise(id: int, db: Session = Depends(get_db)):
    # exe = find_exercise(id)
    exe = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not exe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return exe


@app.post("/exercise", status_code=status.HTTP_201_CREATED, response_model=schemas.Exercise)
async def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    new_exe = models.Exercise(**exercise.dict())
    db.add(new_exe)
    db.commit()
    db.refresh(new_exe)
    return new_exe


@app.put("/exercises/{id}", response_model=schemas.Exercise)
async def update_exercise(id: int, exe: schemas.ExerciseCreate, db: Session = Depends(get_db)):
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


@app.get('/users', status_code=status.HTTP_200_OK, response_model=List[schemas.User])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@app.get('/users/{id}', status_code=status.HTTP_200_OK, response_model=schemas.User)
async def get_users(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found.")
    return user


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.put('/users/{id}', response_model=schemas.User)
async def update_user(id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    update_user_query = db.query(models.User).filter(models.User.id == id)
    user_to_update = update_user_query.first()
    if user_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} does not exist.")
    update_user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return update_user_query.first()


@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)

    if user_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")

    user_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# /repeats {exercise_id}
# /sequences
# /workouts
# /workout-items {foreign keys: exercise_id, repeat_id, workout_id, user_id}
