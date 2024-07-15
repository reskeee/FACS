from db_interaction import *

engine = create_engine("sqlite:///test1.db", echo=True)
session = Session(engine)

Base.metadata.create_all(engine)


with Session(engine) as session:
    user1 = Users(
        name="Руслан",
        surname="Хаирбеков",
        lastname="Чеченец",
        position_id=1,
        age=15,
        location_id=3,
        job_id=2
    )
    user2 = Users(
        name="Мизеахмед",
        surname="бабахов",
        lastname="ывапролдж",
        position_id=4,
        age=17,
        location_id=2,
        job_id=34
    )
    user3 = Users(
        name="длптшз",
        surname="аапрапт",
        lastname="ыыыыыыыыы",
        position_id=15,
        age=1,
        location_id=54,
        job_id=26
    )

    event1 = Events(
        user_id=2,
        location_id=2,
        timestamp = "2024-05-12"
    )  
    event2 = Events(
        user_id=1,
        location_id=4,
        timestamp="2024-03-12"
    )  
    event3 = Events(
        user_id=3,
        location_id=1,
        timestamp="2024-05-14"
    )         

    loc1 = Locations(
        title="Столовая"
    )
    loc2 = Locations(
        title="Офис"
    )
    loc3 = Locations(
        title="Цех"
    )

    dep1 = Departaments(
        title="Рекламный"
    )
    dep2 = Departaments(
        title="HR"
    )
    dep3 = Departaments(
        title="Разработка"
    )

    job1 = Jobs( # 1
        title="Преподаватель"
    )
    job2 = Jobs( # 2
        title="Директор"
    )
    job3 = Jobs( # 3
        title="Работяга"
    )

    session.add_all([
        user1, user2, user3,
        loc1, loc2, loc3,
        event1, event2, event3,
        dep1, dep2, dep3,
        job1, job2, job3
        ])

    session.commit()