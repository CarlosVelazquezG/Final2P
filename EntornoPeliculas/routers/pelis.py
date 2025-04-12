from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from schemas.schemasP import PeliculaCreate, PeliculaResponse
from models.modelsDB import Pelicula
from DB.conexion import Session 

routerPeliculas = APIRouter()

# 1. Crear una película
@routerPeliculas.post("/peliculas", response_model=PeliculaResponse, tags=["Añadir pelicula"])
def crear_pelicula(pelicula: PeliculaCreate):
    db = Session()
    try:
        nueva_pelicula = Pelicula(**pelicula.dict())
        db.add(nueva_pelicula)
        db.commit()
        db.refresh(nueva_pelicula)
        return nueva_pelicula
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear película: {str(e)}")

# 2. Obtener todas las películas
@routerPeliculas.get("/peliculas", response_model=list[PeliculaResponse], tags=["Mostrar todas las peliculas"])
def obtener_peliculas():
    db = Session()
    try:
        return db.query(Pelicula).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener películas: {str(e)}")

# 3. Obtener una película por ID
@routerPeliculas.get("/peliculas/{id}", response_model=PeliculaResponse, tags=["Mostrar una pelicula"])
def obtener_pelicula(id: int):
    db = Session()
    try:
        pelicula = db.query(Pelicula).filter(Pelicula.id == id).first()
        if not pelicula:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return pelicula
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar película: {str(e)}")

# 4. Actualizar una película
@routerPeliculas.put("/peliculas/{id}", response_model=PeliculaResponse, tags=["Actualizar pelicula"])
def actualizar_pelicula(id: int, datos: PeliculaCreate):
    db = Session()
    try:
        pelicula = db.query(Pelicula).filter(Pelicula.id == id).first()
        if not pelicula:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        for key, value in datos.dict().items():
            setattr(pelicula, key, value)
        db.commit()
        db.refresh(pelicula)
        return pelicula
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar película: {str(e)}")

# 5. Eliminar una película
@routerPeliculas.delete("/peliculas/{id}", tags=["Eliminar pelicula"])
def eliminar_pelicula(id: int):
    db = Session()
    try:
        pelicula = db.query(Pelicula).filter(Pelicula.id == id).first()
        if not pelicula:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        db.delete(pelicula)
        db.commit()
        return {"mensaje": "Película eliminada correctamente"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar película: {str(e)}")
