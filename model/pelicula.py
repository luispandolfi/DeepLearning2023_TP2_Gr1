from model.base_model import BaseModel
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import pandas as pd

class Pelicula(BaseModel):
    __tablename__ = "Peliculas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    fecha_estreno: Mapped[datetime]
    url: Mapped[str]
    genero_unknown: Mapped[bool]
    genero_action: Mapped[bool]
    genero_adventure: Mapped[bool]
    genero_animation: Mapped[bool]
    genero_children: Mapped[bool]
    genero_comedy: Mapped[bool]
    genero_crime: Mapped[bool]
    genero_documentary: Mapped[bool]
    genero_drama: Mapped[bool]
    genero_fantasy: Mapped[bool]
    genero_film_noir: Mapped[bool]
    genero_horror: Mapped[bool]
    genero_musical: Mapped[bool]
    genero_mystery: Mapped[bool]
    genero_romance: Mapped[bool]
    genero_sci_fi: Mapped[bool]
    genero_thriller: Mapped[bool]
    genero_war: Mapped[bool]
    genero_western: Mapped[bool]


    GENRES = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
            'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']


    def __init__(self, nombre, fecha_estreno, url, genero_unknown = False, genero_action = False, genero_adventure = False,
                 genero_animation=False, genero_children=False, genero_comedy=False, genero_crime=False,
                 genero_documentary=False, genero_drama=False, genero_fantasy=False, genero_film_noir=False,
                 genero_horror=False, genero_musical=False, genero_mystery=False, genero_romance=False,
                 genero_sci_fi=False, genero_thriller=False, genero_war=False, genero_western=False, id = None):
        self.nombre = nombre
        self.fecha_estreno = pd.to_datetime(fecha_estreno, format="%Y-%m-%d")
        self.url = url
        self.genero_unknown = genero_unknown
        self.genero_action = genero_action
        self.genero_adventure = genero_adventure
        self.genero_animation = genero_animation
        self.genero_children = genero_children
        self.genero_comedy = genero_comedy
        self.genero_crime = genero_crime
        self.genero_documentary = genero_documentary
        self.genero_drama = genero_drama
        self.genero_fantasy = genero_fantasy
        self.genero_film_noir = genero_film_noir
        self.genero_horror = genero_horror
        self.genero_musical = genero_musical
        self.genero_mystery = genero_mystery
        self.genero_romance = genero_romance
        self.genero_sci_fi = genero_sci_fi
        self.genero_thriller = genero_thriller
        self.genero_war = genero_war
        self.genero_western = genero_western
        self.id = id

        
    #unknown no se retorna en la lista, no se uso para entrenar el model
    def get_genres(self):
        return [int(self.genero_action),
                int(self.genero_adventure),
                int(self.genero_animation),
                int(self.genero_children),
                int(self.genero_comedy),
                int(self.genero_crime),
                int(self.genero_documentary),
                int(self.genero_drama),
                int(self.genero_fantasy),
                int(self.genero_film_noir),
                int(self.genero_horror),
                int(self.genero_musical),
                int(self.genero_mystery),
                int(self.genero_romance),
                int(self.genero_sci_fi),
                int(self.genero_thriller),
                int(self.genero_war),
                int(self.genero_western)]