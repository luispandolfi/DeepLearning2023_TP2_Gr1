from model.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

class PrediccionScore(BaseModel):
    __tablename__ = "PrediccionesScore"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int]
    id_pelicula: Mapped[int]
    puntuacion: Mapped[int]


    def __init__(self, id_usuario, id_pelicula, puntuacion, id=None):
        self.id_usuario = id_usuario
        self.id_pelicula = id_pelicula
        self.puntuacion = puntuacion
        self.id = id