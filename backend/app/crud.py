from sqlalchemy.orm import Session
from . import models

def create_operation(db: Session, expr: str, res: float):
    op = models.Operation(expression=expr, result=res)
    db.add(op)
    db.commit()
    db.refresh(op)
    return op

def get_all_operations(db: Session):
    return db.query(models.Operation).order_by(models.Operation.id.desc()).all()
