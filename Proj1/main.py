from fastapi import FastAPI, HTTPException
from enum import Enum


app = FastAPI()


class Department(str, Enum):
    sales = "sales"
    hr = "hr"

EMPLOYEES = [
    {"id": 1, "name": "John", "age": 30, "salary": 50000,"department":"sales"},
    {"id": 2, "name": "Jane", "age": 25, "salary": 60000,"department":"sales"},
    {"id": 3, "name": "Bob", "age": 35, "salary": 70000, "department":"hr"},
    {"id": 4, "name": "Alice", "age": 28, "salary": 80000, "department":"hr"}
]
# get function with dictionory return type

@app.get("/")
async def read_root() -> dict[str,str]:
    return {"Hello": "World"}

#get function about the company which returns string
@app.get("/about")
async def read_about()-> str:
    return "Maran Company - This is all about my Company"

#get function with list return type
@app.get("/employees")
async def read_employees() -> list[dict]:
    return EMPLOYEES

#get function with list return type and id parameter
@app.get("/employees/{id}")
async def read_employee(id: int) -> dict:
   employee = next((emp for emp in EMPLOYEES if emp["id"] == id), None)
   if employee:
       return employee
   else:
       raise HTTPException(status_code=404, detail="Employee not found") 
   
   #get employees based on department
@app.get("/employees/department/{department}")
async def read_employees_by_department(department: Department) -> list[dict]:
    employees = [emp for emp in EMPLOYEES if emp["department"].lower() == department.value]
    if employees:
        return employees
    else:
        raise HTTPException(status_code=404, detail="Employees not found")