from pydantic import BaseModel, EmailStr, AnyUrl

class Person(BaseModel):
    name: str
    age: int = 20
    weight: float
    email: EmailStr
    myurl: AnyUrl

result = Person(name="Balaji", age=24, weight=49.5, email="balajivs@gmail.com", myurl="https://google.com")
print(result.model_dump_json())
print(result)