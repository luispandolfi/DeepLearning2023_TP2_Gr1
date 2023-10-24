from model.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import pandas as pd

class Trabajador(BaseModel):
    __tablename__ = "Trabajadores"
    id: Mapped[int] = mapped_column(primary_key=True)
    puesto: Mapped[str]
    categoria: Mapped[str]
    horario_trabajo: Mapped[str]
    fecha_alta: Mapped[datetime]


    def __init__(self, id, puesto, categoria, horario_trabajo, fecha_alta):
        self.id = id
        self.puesto = puesto
        self.categoria = categoria
        self.horario_trabajo = horario_trabajo
        self.fecha_alta = pd.to_datetime(fecha_alta, format="%Y-%m-%d")