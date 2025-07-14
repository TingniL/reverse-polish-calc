from sqlalchemy import Column, Integer, String, Float, DateTime, func
from .database import Base

class Operation(Base):
    __tablename__ = "operations"

    id          = Column(Integer, primary_key=True, index=True)
    expression  = Column(String, nullable=False)
    result      = Column(Float, nullable=False)
    created_at  = Column(DateTime, server_default=func.now())
