import asyncio
from pprint import pprint
from typing import Optional, List
from sqlalchemy import ForeignKey, String, select, create_engine
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase

STRING_LENGTH = 255


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(STRING_LENGTH))
    surname: Mapped[str] = mapped_column(String(STRING_LENGTH))
    lastname: Mapped[str] = mapped_column(String(STRING_LENGTH))
    position_id: Mapped[int]
    age: Mapped[int]
    location_id: Mapped[int]
    job_id: Mapped[int]

    def __repr__(self) -> str:
        return f"Users(id={self.id!r}, name={self.name!r}, surname={self.surname!r},\
 lastname={self.lastname!r}, position_id={self.position_id!r}, age={self.age!r}, location_id={self.location_id!r})"


class Events(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    location_id: Mapped[int]
    timestamp: Mapped[str]

    def __repr__(self) -> str:
        return f"Events(id={self.id!r}, user_id={self.user_id!r}, location_id={self.location_id!r}, temistamp={self.timestamp!r})"


class Images(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    path: Mapped[str] = mapped_column(String(STRING_LENGTH))

    def __repr__(self) -> str:
        return f"Images(id={self.id!r}, user_id={self.user_id!r}), path={self.path!r}"


class Locations(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(STRING_LENGTH))

    def __repr__(self) -> str:
        return f"Locations(id={self.id!r}, title={self.title!r})"
    

class Departaments(Base):
    __tablename__ = "departaments"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(STRING_LENGTH))

    def __repr__(self) -> str:
        return f"Positions(id={self.id!r}, title={self.title!r})"


class Jobs(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(STRING_LENGTH))

    def __repr__(self) -> str:
        return f"Jobs(id={self.id!r}, title={self.title!r})"


engine = create_engine("sqlite:///test1.db", echo=True)
session = Session(engine)
