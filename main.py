import os
import aiofiles
import datetime as dt
import sqlalchemy.exc
from db_interaction import *
from models import *
# from qdrant_test import *
from fastapi import FastAPI, UploadFile, WebSocket
from fastapi.responses import JSONResponse, FileResponse
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


@app.get("/user/")
async def get_user_data(id: int):
    stmt = select(Users).where(Users.id == id) # Запрос в БД
    user_data = session.scalars(stmt).fetchall()[0]
    # print(user_data)

    # stmt1 = select(Images).where(Images.user_id == id)
    # paths = session.scalar(stmt1).path

    stmt = select(Images)
    paths = [image.path for image in session.scalars(stmt)]

    return JSONResponse({
        "id": user_data.id, 
        "name": user_data.name,
        "surname": user_data.surname,
        "lastname": user_data.lastname,
        "age": user_data.age,
        "departament_id": user_data.departament_id,
        "location_id": user_data.location_id,
        "job_id": user_data.job_id,
        "last_seen": user_data.last_seen,
        "images": paths
    })


@app.get("/users/")
async def get_all_users():
    stmt = select(Users) # Запрос в БД 

    users_list = JSONResponse([{"id": user.id, 
                   "name": user.name, 
                   "surname": user.surname, 
                   "lastname": user.lastname, 
                   "job": user.job_id, 
                   "last_seen": user.last_seen}
                   for user in session.scalars(stmt)])

    return users_list


@app.get("/locations")
async def get_locations():
    stmt = select(Locations) # Запрос в БД

    locations_list = JSONResponse([{"id": location.id,
                        "name": location.name}
                   for location in session.scalars(stmt)])

    return locations_list


@app.get("/departaments") #
async def get_departaments():
    stmt = select(Departaments) # Запрос в БД

    departamenst_list = JSONResponse([{"id": departament.id, 
                          "name": departament.name}
                   for departament in session.scalars(stmt)])

    return departamenst_list


@app.get("/jobs")
async def get_jobs(): 
    stmt = select(Jobs) # Запрос в БД

    jobs_list = JSONResponse([{"id": job.id, 
                  "name": job.name}
                   for job in session.scalars(stmt)])

    return jobs_list


@app.get("/events")
async def get_events():
    stmt = select(Events) # Запрос в БД

    events_list = JSONResponse([{"id": event.id,
                    "user_id": event.user_id,
                    "location_id": event.location_id, 
                    "timestamp": event.timestamp}
                   for event in session.scalars(stmt)])

    return events_list 


@app.get("/images/{id}/{src}")
async def get_image(id: int, src: str):
    return FileResponse(path=f"images/{id}/{src}")

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

    return JSONResponse({"message": "Successful"})


@app.delete("/image/delete")
async def image_delete(id: int):
    record_for_delete = session.get(Users, id)

    image_path = record_for_delete.path

    session.delete(record_for_delete)
    session.commit()

    os.remove(image_path)
    
    return JSONResponse({"message": "Successful"})
    

@app.post("/user/create")
async def add_user(params: UserParams):
    new_user = Users(
        name=params.name,
        surname=params.surname,
        lastname=params.lastname,
        departament_id=params.departament_id,
        age=params.age,
        location_id=params.location_id,
        job_id=params.job_id,
        last_seen=dt.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    )

    session.add(new_user)
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/user/update")
async def update_user(id: int, params: UserParams):
    stmt = select(Users).where(Users.id == id) 
    updated_record = session.scalar(stmt).one()

    updated_record.name = params.name 
    updated_record.surname = params.surname
    updated_record.lastname = params.lastname
    updated_record.departament_id = params.departament_id
    updated_record.age = params.age
    updated_record.location_id = params.location_id
    updated_record.job_id = params.job_id

    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/user/delete")
async def delete_user(params: DeleteParams):
    record_for_delete = session.get(Users, params.id)

    session.delete(record_for_delete)
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/locations/create")
async def create_location(params: CreateParams):
    new_location = Locations(
        title=params.new_title
    )

    session.add(new_location)
    session.commit()


@app.post("/locations/update")
async def update_location(params: UpdateParams):
    stmt = select(Locations).where(Locations.id == params.id)
    updated_record = session.scalars(stmt).one()

    updated_record.title = params.new_title
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/locations/delete")
async def delete_location(params: DeleteParams):
    record_for_delete = session.get(Locations, params.id)
    session.delete(record_for_delete)
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/departaments/create")
async def create_departament(params: CreateParams):
    new_departament = Departaments(
        title=params.new_title
    )

    session.add(new_departament)
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/departaments/update")
async def update_departaments(params: UpdateParams):
    stmt = select(Departaments).where(Departaments.id == params.id)
    updated_record = session.scalars(stmt).one()

    updated_record.title = params.new_title
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/departaments/delete")
async def delete_departaments(params: DeleteParams):
    record_for_delete = session.get(Departaments, params.id)
    session.delete(record_for_delete)
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/jobs/create")
async def create_job(params: CreateParams):
    new_job = Jobs(
        title=params.new_title
    )

    session.add(new_job)
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/jobs/update")
async def update_jobs(params: UpdateParams):
    stmt = select(Jobs).where(Jobs.id == params.id)
    updated_record = session.scalars(stmt).one()

    updated_record.title = params.new_title
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/jobs/delete")
async def delete_jobs(params: DeleteParams):
    record_for_delete = session.get(Jobs, params.id)
    session.delete(record_for_delete)
    session.commit()

    return JSONResponse({"message": "Successful"})


@app.post("/events/add")
async def add_event(params: AddEvent):
    new_event = Events(
        user_id=params.user_id,
        location_id=params.location_id,
        timestamp=params.timestamp
    )

    session.add(new_event)
    session.commit()
    
    return JSONResponse({"message": "Successful"})


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()


# @app.post("/api/display")
# async def frame_interaction(image):
#     pass


# @app.post("/api/embedding")
# async def embedding_interaction(location_id: int, timestamp, embedding):
#     result = await min_distance(embedding=embedding)[0] # TODO loc_id и timtstamp приходят. Нужно доставать user_id(payload)

#     new_event = Events(
#         location_id=location_id,
#         timestamp=timestamp,
#         # TODO User_id
#     )

#     return result

async def update_lastseen(user_id: int, new_lastseen: str):
    updated_record = session.get(Users, user_id)

    updated_record.last_seen = new_lastseen
    session.commit()

# if __name__ == "__main__":
#     update_lastseen(3, "17-07-2024 16:03:41")