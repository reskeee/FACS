from pydantic import BaseModel


class UserParams(BaseModel):
    name: str
    surname: str
    lastname: str
    age: int
    departament_id: int
    location_id: int
    job_id: int


class UserDeleteParams(BaseModel):
    id: int


class EventParams(BaseModel):
    pass # TODO 
