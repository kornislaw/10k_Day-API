from typing import Optional

from pydantic import BaseModel


class Exercise(BaseModel):
    name: str
    description: Optional[str]