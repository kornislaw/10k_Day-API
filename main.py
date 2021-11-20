from typing import Optional

from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Exercise(BaseModel):
    name: str
    description: Optional[str]


stored_exercises = [
    {"id": 1, "name": "The best exercise ever", "description": "Here's why: ..."},
    {"id": 2, "name": "Second best exercise", "description": "Just after the first one..."},
]


def find_exercise(id):
    for exe in stored_exercises:
        if exe["id"] == int(id):
            return exe
    return None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/exercises")
async def get_exercises():
    return {"data": stored_exercises}


@app.get("/exercises/{id}")
async def get_exercise(id: int):
    exe = find_exercise(id)
    if not exe:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"ID {id} not found")
    return exe


@app.post("/exercise", status_code=status.HTTP_201_CREATED)
async def post_exercise(exercise: Exercise):
    # return {"Exercise": f"{exercise}"}
    next_id = max([exe["id"] for exe in stored_exercises]) + 1
    stored_exercises.append({"id": next_id,
                             "name": exercise.name,
                             "description": exercise.description})
    return exercise.dict()


# /exercises
# /repeats {exercise_id}
# /sequences
# /workouts
# /workout-items {foreign keys: exercise_id, repeat_id, workout_id, user_id}
# /users
