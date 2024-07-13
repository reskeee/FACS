from fastapi import FastAPI, UploadFile
import aiofiles
from db_interaction import *

app = FastAPI()

@app.get("/")
async def page():
    #TODO
    return


@app.get("/user/")
async def get_user_data(id: int):
    stmt = select(Users).where(Users.id == id) # Запрос в БД

    user_data = await session.scalars(stmt).fetchall()[0]
    return {
        "id": user_data.id,
        "name": user_data.name,
        "surname": user_data.surname,
        "lastname": user_data.lastname,
        "position_id": user_data.position_id,
        "age": user_data.age,
        "location_id": user_data.location_id,
        "job_id": user_data.job_id
    }


@app.get("/users/")
async def get_all_users():
    stmt = select(Users) # Запрос в БД

    users_list = [{"id": user.id, "name": user.name, "surname": user.surname, "lastname": user.lastname, "job": user.job_id}
                   for user in session.scalars(stmt)]

    return users_list


@app.get("/locations")
async def get_locations():
    stmt = select(Locations) # Запрос в БД

    locations_list = [{"id": location.id, "name": location.name}
                   for location in session.scalars(stmt)]

    return locations_list


@app.get("/departaments")
async def get_departaments():
    stmt = select(Departaments) # Запрос в БД

    departamenst_list = [{"id": departament.id, "name": departament.name}
                   for departament in session.scalars(stmt)]

    return departamenst_list


@app.get("/jobs")
async def get_jobs():
    stmt = select(Jobs) # Запрос в БД

    jobs_list = [{"id": job.id, "name": job.name}
                   for job in session.scalars(stmt)]

    return jobs_list


@app.put("/put_image/")
async def upload_image(file: UploadFile, user_id: int): #TODO Сделать запись в БД
    async with aiofiles.open("C:/Users/reskeee/Desktop/GazpronmProject/test/test.png", "wb") as out_file:
        content = await file.read()
        await out_file.write(content)


@app.post("/create_location")
async def create_location(new_title: str):
    new_location = Locations(
        title=new_title
    )

    session.add(new_location)
    session.commit()


@app.post("/update_location")
async def update_location(id: int, new_title: str):
    stmt = select(Locations).where(Locations.id == id)
    updated_record = session.scalars(stmt).one()

    updated_record.title = new_title
    session.commit()


@app.post("/delete_location")
async def delete_location(id: int):
    record_for_delete = session.get(Locations, id)
    session.delete(record_for_delete)
    session.commit()


@app.post("/create_departament")
async def create_departament(new_title: str):
    new_departament = Departaments(
        title=new_title
    )

    session.add(new_departament)
    session.commit()


@app.post("/update_departaments")
async def update_departaments(id: int, new_title: str):
    stmt = select(Departaments).where(Departaments.id == id)
    updated_record = session.scalars(stmt).one()

    updated_record.title = new_title
    session.commit()


@app.post("/delete_departaments")
async def delete_departaments(id: int):
    record_for_delete = session.get(Departaments, id)
    session.delete(record_for_delete)
    session.commit()


@app.post("/create_job")
async def create_job(new_title: str):
    new_job = Jobs(
        title=new_title
    )

    session.add(new_job)
    session.commit()


@app.post("/update_jobs")
async def update_jobs(id: int, new_title: str):
    stmt = select(Jobs).where(Jobs.id == id)
    updated_record = session.scalars(stmt).one()

    updated_record.title = new_title
    session.commit()


@app.post("/delete_jobs")
async def delete_jobs(id: int):
    record_for_delete = session.get(Jobs, id)
    session.delete(record_for_delete)
    session.commit()

