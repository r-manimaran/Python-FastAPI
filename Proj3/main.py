from fastapi import FastAPI, HTTPException
from enum import Enum
from schemas import Department, Employee

app = FastAPI()

###### Proj3 - Added Query parameters to the employees endopoint

Employees =[
            {"id":1,"name":"Amit","department":"sales","age":24,"salary":"4000","skills":[
                {"id":1,"name":"python","level":8},
                {"id":2,"name":"java","level":4}
            ]},
            {"id":2,"name":"Rahul","department":"sales","age":25,"salary":"5000","skills":[]},
            {"id":3,"name":"Rohit","department":"hr","age":26,"salary":"6000","skills":[]},
            {"id":4,"name":"Rajesh","department":"hr","age":27,"salary":"7000","skills":[]},
            {"id":5,"name":"Rakesh","department":"sales","age":28,"salary":"8000","skills":[]}]


#get all the employees with query parameters
@app.get("/employees")
async def read_employees(department: Department |None =None,
                         age: int |None=None
                         )->list[Employee]:
    
    employees_list = [Employee(**e) for e in Employees]
    # filter the employees based on the query parameters
    if department is not None:
        employees_list = [emp for emp in Employees if emp["department"].lower() == department.value]
    if age is not None:
        employees_list = [emp for emp in Employees if emp["age"] == age]
        
    if employees_list:
        return employees_list
    else:
        raise HTTPException(status_code=404, detail="Employees not found")
                            
   
@app.get("/employees")
async def read_employees()->list[Employee]:
    return [
        Employee(**e) for e in Employees
    ]
#this needs to be declared first, otherwise /employees/{employee_id} get higher precendance
@app.get("/employees/me")
def read_user_me():
    return {"user_id": "the current user"}

##get a employee based on Id
@app.get("/employees/{employee_id}")
async def read_employee(employee_id: int)->Employee:
    employee = next((emp for emp in Employees if emp["id"] == employee_id), None)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

#get a employee based on department
@app.get("/employees/department/{department}")
async def read_employees_by_department(department: Department)->list[Employee]:
    employees = [emp for emp in Employees if emp["department"].lower() == department.value]
    if employees:
        return employees
    else:
        raise HTTPException(status_code=404, detail="Employees not found")   
    

    #notes
    # to run the app use uvicorn main:app --reload
    # to run the app in debug mode use uvicorn main:app --reload --debug
    # to run the app in debug mode use uvicorn main:app --reload --debug --host 0.0.0.0 --port 8000