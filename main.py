from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Exercise(BaseModel):
    name: str
    description: str


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/exercises")
async def get_exercises():
    return {"Exercises": f""}


@app.post("/exercise")
async def post_exercise(exercise: Exercise):
    return {"Exercise": f"{exercise}"}


# /exercises
# /repeats {exercise_id}
# /sequences
# /workouts
# /workout-items {foreign keys: exercise_id, repeat_id, workout_id, user_id}
# /users
