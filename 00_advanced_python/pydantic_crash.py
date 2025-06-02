from typing import Annotated, Literal

from annotated_types import Gt

from pydantic import BaseModel, ValidationError

# ------------------------------------------------------------
# 1. Annotated Types
# ------------------------------------------------------------
# class Fruit(BaseModel):
#     name: str  
#     color: Literal['red', 'green']  
#     weight: Annotated[float, Gt(0)]  
#     bazam: dict[str, list[tuple[int, bool, float]]]

# fruit = Fruit(name="apple", color="red", weight=1.0, bazam={"a": [(1, True, 1.0)]})

# print(fruit)

# try:
#     fruit = Fruit(name="apple", color="red", weight=0.0, bazam={"a": [(1, True, 1.0)]})
# except ValidationError as e:
#     print(e)

# ------------------------------------------------------------
# 2. Frozen Models
# ------------------------------------------------------------
# class Model(BaseModel, frozen=True):
#     a: str
    
    
# model = Model(a="a")
# print(model)

# try:
#     model.a = "b"
# except Exception as e:
#     print(e)

# ------------------------------------------------------------
# 3. Ellipsis (...) in Models
# ------------------------------------------------------------

from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(...)  # required
    age: int = Field(default=18)  # optional, default is 18

test = User(name="John")
print(test)

test = User(name="John", age=20)
print(test)

test = User(name="John", age=20, email="john@example.com")
print(test)

try:
    test = User( age=20, email="john@example.com", address="123 Main St", phone="1234567890")
except ValidationError as e:
    print(e)

