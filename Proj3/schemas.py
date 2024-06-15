from datetime import date
from enum import Enum
from pydantic import BaseModel, Field

class Department(str, Enum):
    sales = "sales"
    hr = "hr"
    finance = "finance"

#Model for Skillset
class Skillset(BaseModel):
    id: int = Field(default=None, ge=1)
    name: str = Field(min_length=3, max_length=50)
    level: int = Field(gt=0)

#Model for Employee
class Employee(BaseModel):
    id: int = Field(default=None, ge=1)
    name: str = Field(min_length=3, max_length=50)
    department: Department = Field(default=Department.sales)
    salary: int = Field(gt=0)
    dateofjoin: date = Field(default_factory=date.today)
    skills: list[Skillset] = Field(default=[])



