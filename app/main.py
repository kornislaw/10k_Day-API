from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Exercise(BaseModel):
    name: str
    description: Optional[str]


try:
    conn = psycopg.connect(
        "host=localhost dbname=10kday user=postgres password=postgres"
    )
    cursor = conn.cursor(row_factory=psycopg.rows.dict_row)
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


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "Success"}


@app.get("/exercises")
async def get_exercises():
    cursor.execute("""SELECT * FROM exercises ORDER BY id""")
    data = cursor.fetchall()
    return {"data": data}


@app.get("/exercises/{id}")
async def get_exercise(id: int):
    exe = find_exercise(id)
    if not exe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return exe


@app.post("/exercise", status_code=status.HTTP_201_CREATED)
async def post_exercise(exercise: Exercise):
    cursor.execute(
        """INSERT INTO exercises (name, description) VALUES (%s, %s) RETURNING *""",
        (exercise.name, exercise.description),
    )
    new_exe = cursor.fetchone()
    conn.commit()
    return new_exe


@app.put("/exercises/{id}")
async def update_exercise(id: int, exe: Exercise):
    cursor.execute(
        """UPDATE exercises SET name=%s, description=%s WHERE id=%s RETURNING *""",
        (
            exe.name,
            exe.description,
            str(id),
        ),
    )
    updated_exe = cursor.fetchone()
    if updated_exe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise ID {id} does not exist",
        )
    conn.commit()
    return updated_exe


@app.delete("/exercises/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute("""DELETE FROM exercises WHERE id=%s RETURNING *""", (id,))
    deleted_exe = cursor.fetchone()
    if deleted_exe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Exercise ID {id} does not exist",
        )
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# /exercises
# /repeats {exercise_id}
# /sequences
# /workouts
# /workout-items {foreign keys: exercise_id, repeat_id, workout_id, user_id}
# /users
