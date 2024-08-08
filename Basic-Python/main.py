# Data Types as annotation
number: int =10
decimal: float = 10.5
boolean: bool = True
text: str = "Hello World"

names:list = ["John", "Mary", "Peter"]
coordinates:tuple = (10, 20) # immutable list
ages: frozenset = {10, 20, 30} # immutable set
person:dict = {"name": "John", "age": 30} # dictionary for key value pairs
unique: set = {1, 2, 3} # same as list but without duplicates

# constants
from typing import Final
PI: Final[float] = 3.14
VERSION: Final[str] = "1.0.0"

#reusable code
from datetime import datetime
print(datetime.now())

# instead use this way, here we are using a method
def get_current_time() -> datetime:
    return datetime.now()

print(get_current_time())

#retun type for a function
def add_numbers(a: int, b: int) -> int:
    return a + b

#return None
def log_message(message: str) -> None:
    print(message)

# defining class and methods
class Person:
    # used to intialize the class
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age

    # self refers to the instance of the class
    def greet(self) -> str:
        return f"Hello, my name is {self.name} and I'm {self.age} years old."
    
user1: Person = Person("John", 30)
print(user1.greet())

# Dunder methods
class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __add__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"