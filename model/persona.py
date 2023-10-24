from model.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

class Persona(BaseModel):
    __tablename__ = "Personas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre_completo: Mapped[str]
    anio_nacimiento: Mapped[int]
    genero: Mapped[str]
    codigo_postal: Mapped[str]


    def __init__(self, nombre_completo, anio_nacimiento, genero, codigo_postal, id = None):
        self.nombre_completo = nombre_completo
        self.anio_nacimiento = anio_nacimiento
        self.genero = genero
        self.codigo_postal = codigo_postal
        self.id = id