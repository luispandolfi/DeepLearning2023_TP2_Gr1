from model.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import pandas as pd

class Usuario(BaseModel):
    __tablename__ = "Usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    ocupacion: Mapped[str]
    fecha_alta: Mapped[datetime]


    def __init__(self, id, ocupacion, fecha_alta):
        self.id = id
        self.ocupacion = ocupacion
        self.fecha_alta = pd.to_datetime(fecha_alta, format="%Y-%m-%d")