from pydantic import BaseModel
from datetime import datetime
from typing import List

class ExpressionIn(BaseModel):
    expression: str

class BatchExpressionIn(BaseModel):
    expressions: List[str]

class OperationOut(BaseModel):
    id: int
    expression: str
    result: float
    created_at: datetime

    class Config:
        from_attributes = True
