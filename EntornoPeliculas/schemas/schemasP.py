from pydantic import BaseModel, Field

# Esquema base para validar lo que llega
class PeliculaCreate(BaseModel):
    title: str = Field(..., min_length=2)
    genre: str = Field(..., min_length=4)
    year: int = Field(..., ge=1000, le=9999)
    clss: str = Field(..., min_length=1, max_length=1)


