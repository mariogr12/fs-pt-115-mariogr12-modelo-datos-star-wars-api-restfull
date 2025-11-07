from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Tabla intermedia N:M
user_favorite_characters = Table(
    "user_favorite_characters",
    db.Model.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50))

    favorite_characters: Mapped[list["Character"]] = relationship(
        "Character",
        secondary=user_favorite_characters,
        back_populates="favorited_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "favorite_characters": [character.id for character in self.favorite_characters]
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    species: Mapped[str] = mapped_column(String(50))
    gender: Mapped[str] = mapped_column(String(50))
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"))

    planet: Mapped["Planet"] = relationship("Planet", back_populates="characters")
    favorited_by: Mapped[list["User"]] = relationship(
        "User",
        secondary=user_favorite_characters,
        back_populates="favorite_characters"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "gender": self.gender,
            "planet": self.planet.name if self.planet else None
        }

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    climate: Mapped[str] = mapped_column(String(50))
    terrain: Mapped[str] = mapped_column(String(50))
    population: Mapped[str] = mapped_column(String(50))

    characters: Mapped[list["Character"]] = relationship("Character", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "characters": [c.id for c in self.characters]
        }

class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"))

    character: Mapped["Character"] = relationship("Character", back_populates="vehicles")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "pilot": self.character.name if self.character else None
        }

Character.vehicles = relationship("Vehicle", back_populates="character")