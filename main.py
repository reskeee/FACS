import os
import aiofiles
import datetime as dt
import sqlalchemy.exc
from db_interaction import *
from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def page():
    #TODO
    return


@app.get("/user")
async def get_user_data(id: int):
    stmt = select(Users).where(Users.id == id) # Запрос в БД

    user_data = await session.scalars(stmt).fetchall()[0]
    return {
        "id": user_data.id,
        "name": user_data.name,
        "surname": user_data.surname,
        "lastname": user_data.lastname,
        "age": user_data.age,
        "position_id": user_data.position_id,
        "location_id": user_data.location_id,
        "job_id": user_data.job_id,
        "last_seen": user_data.last_seen
    }


@app.get("/users")
async def get_all_users():
    stmt = select(Users) # Запрос в БД

    users_list = [{"id": user.id, 
                   "name": user.name, 
                   "surname": user.surname, 
                   "lastname": user.lastname, 
                   "job": user.job_id, 
                   "last_seen": user.lasst_seen}
                   for user in session.scalars(stmt)]

    return users_list


@app.get("/locations")
async def get_locations():
    stmt = select(Locations) # Запрос в БД

    locations_list = [{"id": location.id,
                        "name": location.name}
                   for location in session.scalars(stmt)]

    return locations_list


@app.get("/departaments")
async def get_departaments():
    stmt = select(Departaments) # Запрос в БД

    departamenst_list = [{"id": departament.id, 
                          "name": departament.name}
                   for departament in session.scalars(stmt)]

    return departamenst_list


@app.get("/jobs")
async def get_jobs():
    stmt = select(Jobs) # Запрос в БД

    jobs_list = [{"id": job.id, 
                  "name": job.name}
                   for job in session.scalars(stmt)]

    return jobs_list


@app.get("/events")
async def get_events():
    stmt = select(Events) # Запрос в БД

    events_list = [{"id": event.id,
                    "user_id": event.user_id,
                    "location_id": event.location_id, 
                    "timestamp": event.timestamp}
                   for event in session.scalars(stmt)]

    return events_list 


@app.get("/image")
async def get_image(id: int):
    try:
        stmt = select(Images).where(Images.id == id)
        image_path = session.scalars(stmt).one().path

    # async with aiofiles.open()
        return image_path
    except sqlalchemy.exc.NoResultFound:
        return "No result found"
    

@app.put("/image/put") 
async def upload_image(file: UploadFile, user_id: int):
    if not (str(user_id) in os.listdir('images')):
        os.mkdir(f'images/{user_id}')

    filepath = f"images/{user_id}/{file.filename}"
    async with aiofiles.open(filepath, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    new_image_path = Images(
        user_id=user_id,
        path=filepath
    )

    session.add(new_image_path)
    session.commit()


@app.delete("/image/delete")
async def image_delete(id: int):
    record_for_delete = session.get(Users, id)

    image_path = record_for_delete.path

    session.delete(record_for_delete)
    session.commit()

    os.remove(image_path)


@app.post("/user/create")
async def add_user(name: str, surname: str, lastname: str, position_id: int, 
                   age: int, location_id: int, job_id: int, last_seen: str):
    new_user = Users(
        name=name,
        surname=surname,
        lastname=lastname,
        position_id=position_id,
        age=age,
        location_id=location_id,
        job_id=job_id,
        last_seen=last_seen
    )

    session.add(new_user)
    session.commit()


@app.post("/user/update")
async def update_user(id: int, name: str, surname: str, lastname: str, 
                      position_id: int, age: int, location_id: int, job_id: int):
    stmt = select(Users).where(Users.id == id) 
    updated_record = session.scalar(stmt).one()

    updated_record.name = name 
    updated_record.surname = surname
    updated_record.lastname = lastname
    updated_record.position_id = position_id
    updated_record.age = age
    updated_record.location_id = location_id
    updated_record.job_id = job_id

    session.commit()


@app.post("/user/delete")
async def delete_user(id: int):
    record_for_delete = session.get(Users, id)
    session.delete(record_for_delete)
    session.commit()


@app.post("/locations/create")
async def create_location(new_title: str):
    new_location = Locations(
        title=new_title
    )

    session.add(new_location)
    session.commit()


@app.post("/locations/update")
async def update_location(id: int, new_title: str):
    stmt = select(Locations).where(Locations.id == id)
    updated_record = session.scalars(stmt).one()

    updated_record.title = new_title
    session.commit()


@app.post("/locations/delete")
async def delete_location(id: int):
    record_for_delete = session.get(Locations, id)
    session.delete(record_for_delete)
    session.commit()


@app.post("/departaments/create")
async def create_departament(new_title: str):
    new_departament = Departaments(
        title=new_title
    )

    session.add(new_departament)
    session.commit()


@app.post("/departaments/update")
async def update_departaments(id: int, new_title: str):
    stmt = select(Departaments).where(Departaments.id == id)
    updated_record = session.scalars(stmt).one()

    updated_record.title = new_title
    session.commit()


@app.post("/departaments/delete")
async def delete_departaments(id: int):
    record_for_delete = session.get(Departaments, id)
    session.delete(record_for_delete)
    session.commit()


@app.post("/jobs/create")
async def create_job(new_title: str):
    new_job = Jobs(
        title=new_title
    )

    session.add(new_job)
    session.commit()


@app.post("/jobs/update")
async def update_jobs(id: int, new_title: str):
    stmt = select(Jobs).where(Jobs.id == id)
    updated_record = session.scalars(stmt).one()

    updated_record.title = new_title
    session.commit()


@app.post("/jobs/delete")
async def delete_jobs(id: int):
    record_for_delete = session.get(Jobs, id)
    session.delete(record_for_delete)
    session.commit()


@app.post("/events/add")
async def add_event(user_id: int, location_id: int, timestamp: str):
    new_event = Events(
        user_id=user_id,
        location_id=location_id,
        timestamp=timestamp
    )

    session.add(new_event)
    session.commit()


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()