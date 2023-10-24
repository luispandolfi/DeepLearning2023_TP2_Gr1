from model.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import pandas as pd

class Score(BaseModel):
    __tablename__ = "Scores"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int]
    id_pelicula: Mapped[int]
    puntuacion: Mapped[int]
    fecha: Mapped[datetime]


    def __init__(self, id_usuario, id_pelicula, puntuacion, fecha, id=None):
        self.id_usuario = id_usuario
        self.id_pelicula = id_pelicula
        self.puntuacion = puntuacion
        self.fecha = pd.to_datetime(fecha, format="%Y-%m-%d")
        self.id = id