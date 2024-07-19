from pydantic import BaseModel


class UserParams(BaseModel):
    name: str
    surname: str
    lastname: str
    age: int
    departament_id: int
    location_id: int
    job_id: int


class CreateParams(BaseModel):
    new_title: str


class DeleteParams(BaseModel):
    id: int


class UpdateParams(BaseModel):
    id: int
    new_title: str 


class AddEvent(BaseModel):
    user_id: int
    location_id: int
    timestamp: str


class EventParams(BaseModel):
    pass # TODO 
