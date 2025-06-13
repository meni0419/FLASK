from datetime import datetime
from pprint import pprint

from pydantic import BaseModel, Field

"""
🟦 ЗАДАЧА 1: Patient с alias и default_factory
Создать базовую модель пациента с алиасами для
first_name и last_name(CamelCase), и автоматическим временем регистрации.
Требования:
Поля: first_name, last_name (алиасы: firstName, lastName)
Поле registration_time: генерируется автоматически через default_factory
Включить populate_by_name = True
Добавить описание в json_schema_extra
"""


class Patient(BaseModel):
    id: int
    first_name: str = Field(..., min_length=3, alias="firstName")
    last_name: str = Field(..., min_length=3, alias="lastName")
    age: int
    gender: str
    registration_time: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "title": "Patient Information",
            "description": "A model representing patient data with automatic registration time",
            "example": {
                "id": 1,
                "firstName": "John",
                "lastName": "Smith",
                "age": 30,
                "gender": "Male",
                "registration_time": "2025-06-13 11:09:53"
            }
        }}


class getPatients(Patient):
    id: int
    firstName: str = Field(..., min_length=3, alias="firstName")
    lastName: str = Field(..., min_length=3, alias="lastName")
    age: int
    gender: str
    registration_time: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    patient = Patient(id=1, firstName="Max", lastName="Melnychuk", age=36, gender="Male")
    print("\n\033[94mPatient Information:\033[0m")
    print("\033[90m" + "-" * 50 + "\033[0m")
    print(patient)
    print("\n\033[94mModel Dump JSON:\033[0m")
    print("\033[90m" + "-" * 50 + "\033[0m")
    pprint(patient.model_dump_json())
    print("\n\033[94mModel Dump:\033[0m")
    print("\033[90m" + "-" * 50 + "\033[0m")
    pprint(patient.model_dump())
    print("\n\033[94mJSON Schema:\033[0m")
    print("\033[90m" + "-" * 50 + "\033[0m")
    pprint(patient.model_json_schema())
    print("\033[90m" + "-" * 50 + "\033[0m")
