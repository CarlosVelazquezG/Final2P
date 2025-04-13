from fastapi import FastAPI
from DB.conexion import Base, engine
from routers.pelis import routerPeliculas
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(
    title="API Películas", 
    version="1.0"
)

app.add_middleware(  
    CORSMiddleware,  
    allow_origins=["http://127.0.0.1:5000"], 
    allow_methods=["*"],  
    allow_headers=["*"],  
)  

app.include_router(routerPeliculas)

Base.metadata.create_all(bind=engine)

@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "API Películas"}
