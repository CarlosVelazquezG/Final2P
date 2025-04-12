from fastapi import FastAPI
from DB.conexion import Base, engine
from routers.pelis import routerPeliculas

# Crear instancia de FastAPI
app = FastAPI(
    title="API Películas", 
    version="1.0"
)

# Incluir rutas desde el archivo de rutas
app.include_router(routerPeliculas)

# Crear las tablas en la BD si no existen
Base.metadata.create_all(bind=engine)

# Ruta raíz de prueba
@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API Películas"}
