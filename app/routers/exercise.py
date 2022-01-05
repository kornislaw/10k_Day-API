from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, oath2
from ..database import get_db

router = APIRouter(prefix='/exercises', tags=['Exercises'])


@router.get("/", response_model=List[schemas.Exercise])
async def get_exercises(db: Session = Depends(get_db)):
    execs = db.query(models.Exercise).all()
    return execs


@router.get("/{id}", response_model=schemas.Exercise)
async def get_exercise(id: int, db: Session = Depends(get_db)):
    # exe = find_exercise(id)
    exe = db.query(models.Exercise).filter(models.Exercise.id == id).first()
    if not exe:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} not found"
        )
    return exe


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Exercise)
async def create_exercise(
        exercise: schemas.ExerciseCreate,
        db: Session = Depends(get_db),
        user_id: int = Depends(oath2.get_current_user)
    ):
    print(user_id)
    new_exe = models.Exercise(**exercise.dict())
    db.add(new_exe)
    db.commit()
    db.refresh(new_exe)
    return new_exe


@router.put("/{id}", response_model=schemas.Exercise)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
