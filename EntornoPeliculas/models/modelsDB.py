from DB.conexion import Base
from sqlalchemy import Column, Integer, String

class Pelicula(Base):
    __tablename__ = "peliculas"

    id = Column(Integer, primary_key=True, autoincrement="auto")
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    clss = Column(String(1), nullable=False)