from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ExerciseBase(BaseModel):
    name: str
    description: Optional[str]


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

