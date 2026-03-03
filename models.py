from enum import Enum
from typing import Optional
from uuid import uuid4
from datetime import datetime

from sqlmodel import SQLModel, Field


class PrintType(str, Enum):
    black_white = "black_white"
    colored = "colored"
    photo = "photo"


class Order(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str
    pages: int
    print_type: PrintType
    filename: Optional[str] = None
    status: str = Field(default="pending")
    cost: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
