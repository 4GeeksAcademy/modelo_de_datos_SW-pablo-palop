from flask_sqlalchemy import SQLAlchemy
from typing import List
from sqlalchemy import String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

class Favorite(db.Model):
    __tablename__ = "favorites"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey('characters.id'), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey('planets.id'), nullable=True)
    starship_id: Mapped[int] = mapped_column(ForeignKey('starships.id'), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="favorites")
    character: Mapped["Characters"] = relationship("Characters", back_populates="favorites", foreign_keys=[character_id])
    planet: Mapped["Planets"] = relationship("Planets", back_populates="favorites", foreign_keys=[planet_id])
    starship: Mapped["Starships"] = relationship("Starships", back_populates="favorites", foreign_keys=[starship_id])

class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    nickname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(), default=func.now())
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates = "user")

class Characters(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    group_type: Mapped[str] = mapped_column(String(120), nullable=False)

    planets: Mapped[List["Planets"]] = relationship("Planets", back_populates="character")
    starship: Mapped["Starships"] = relationship("Starships", back_populates="character", uselist=False)
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="character")

class Planets(db.Model):
    __tablename__ = "planets"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    group_type: Mapped[str] = mapped_column(String(120), nullable=False)

    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), nullable=False)
    character: Mapped["Characters"] = relationship("Characters", back_populates="planets")
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="planet")

class Starships(db.Model):
    __tablename__ = "starships"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    group_type: Mapped[str] = mapped_column(String(120), nullable=False)

    character_id: Mapped[int] = mapped_column(ForeignKey("characters.id"), unique=True)
    character: Mapped["Characters"] = relationship("Characters", back_populates="starship")
    favorites: Mapped[List["Favorite"]] = relationship("Favorite", back_populates="starship")