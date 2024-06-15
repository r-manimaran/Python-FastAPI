from datetime import date
from enum import Enum
from pydantic import BaseModel, Field, field_validator

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
class EmployeeBase(BaseModel):  
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(gt=18)
    department: Department = Field(default=Department.sales)
    salary: int = Field(gt=0)
    dateofjoin: date = Field(default_factory=date.today)
    skills: list[Skillset] = Field(default=[])

class EmployeeCreate(EmployeeBase):
    @field_validator("salary")
    def validate_salary(cls, v):
        if v < 1000:
            raise ValueError("Salary must be greater than 5000")
        return v
    @field_validator("age")
    def validate_age(cls, v):
        if v < 18 and v >70:
            raise ValueError("Age must be between 18 and 70")
        return v
    
class Employee(EmployeeBase):
    id: int
    


