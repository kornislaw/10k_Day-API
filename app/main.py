import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine

from .routers import user, exercise, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# app.router.redirect_slashes = False


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


app.include_router(user.router)
app.include_router(exercise.router)
app.include_router(auth.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}






# /repeats {exercise_id}
# /sequences
# /workouts
# /workout-items {foreign keys: exercise_id, repeat_id, workout_id, user_id}
