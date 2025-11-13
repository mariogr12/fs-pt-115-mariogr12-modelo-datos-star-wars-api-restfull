from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

user_favorite_characters = Table(
    "user_favorite_characters",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)

user_favorite_planets = Table(
    "user_favorite_planets",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("planet_id", ForeignKey("planet.id"), primary_key=True),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)

    favorite_planets: Mapped[list['Planet']] = relationship(
        secondary='user_favorite_planets'
    )

    favorite_characters: Mapped[list['Character']] = relationship(
        secondary='user_favorite_characters'
    )

    def serialize(self):
        return{
            "id": self.id,
            "username": self.username,

            "favorite_planets": [planet.serialize() for planet in self.favorite_planets],
            "favorite_characters": [character.serialize() for character in self.favorite_characters]
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name
        }