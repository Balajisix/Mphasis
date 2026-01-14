from pydantic import BaseModel, EmailStr, AnyUrl, field_validator, ValidationError

class Person(BaseModel):
    name: str
    age: int = 20
    weight: float
    email: EmailStr
    myurl: AnyUrl

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    
try:
    person1 = Person(
        name="Balaji",
        age=24,
        weight=49.5,
        email="balaji@gmail.com",
        myurl="https://google.com"
    )
    print(person1.model_dump_json())
except ValidationError as e:
    print("Validation Error: \n", e)

# print(result.model_dump_json())
# print(result)