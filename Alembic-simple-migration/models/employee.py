from sqlalchemy import Column, BIGINT, VARCHAR,String,DateTime,func
from sqlalchemy.orm import relationship

from database import Base
from sqlalchemy import ForeignKey
class Employee(Base):
    __tablename__ = "employees"

    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(VARCHAR(30), nullable=False)
    email = Column(VARCHAR(30), unique= True,nullable=False)
    created_by = Column(String(50), nullable=False)
    created_on = Column(DateTime, default=func.now())

    def __repr__(self):
        return f"id: {self.id}, Employee: {self.name}"
  