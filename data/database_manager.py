from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from data.data_frame_loader import DataFrameLoader
from model.base_model import BaseModel
from model.persona import Persona
from model.usuario import Usuario
from model.trabajador import Trabajador
from model.pelicula import Pelicula
from model.score import Score
from model.prediccion_score import PrediccionScore


class DatabaseManager:

    def __init__(self, connectionString):
        self.engine = create_engine(connectionString)


    def create_database(self):
        BaseModel.metadata.create_all(self.engine)


    def load_initial_data(self):
        dfs = DataFrameLoader.load_all("csv_files/personas.csv","csv_files/trabajadores.csv","csv_files/usuarios.csv","csv_files/peliculas.csv","csv_files/scores.csv")
        session = Session(self.engine)
        self.load_personas(dfs[0], session)
        self.load_trabajadores(dfs[1], session)
        self.load_usuarios(dfs[2], session)
        self.load_peliculas(dfs[3], session)
        self.load_scores(dfs[4], session)
        session.commit()
        session.close()


    def load_personas(self, df, session):
        for row in df.itertuples():
            persona = Persona(
                id = row[1],
                nombre_completo = row[2],
                anio_nacimiento = row[3],
                genero = row[4],
                codigo_postal = row[5]
            )
            session.add(persona)


    def load_trabajadores(self, df, session):
        for row in df.itertuples():
            trabajador = Trabajador(
                id = row[1],
                puesto = row[2],
                categoria = row[3],
                horario_trabajo = row[4],
                fecha_alta = row[5]
            )
            session.add(trabajador)


    def load_usuarios(self, df, session):
        for row in df.itertuples():
            usuario = Usuario(
                id = row[1],
                ocupacion = row[2],
                fecha_alta = row[3]
            )
            session.add(usuario)


    def load_peliculas(self, df, session):
        for row in df.itertuples():
            pelicula = Pelicula(
                id = row[1],
                nombre = row[2],
                fecha_estreno = row[3],
                url = row[4],
                genero_unknown = row[5],
                genero_action = row[6],
                genero_adventure = row[7],
                genero_animation = row[8],
                genero_children = row[9],
                genero_comedy = row[10],
                genero_crime = row[11],
                genero_documentary = row[12],
                genero_drama = row[13],
                genero_fantasy = row[14],
                genero_film_noir = row[15],
                genero_horror = row[16],
                genero_musical = row[17],
                genero_mystery = row[18],
                genero_romance = row[19],
                genero_sci_fi = row[20],
                genero_thriller = row[21],
                genero_war = row[22],
                genero_western = row[23],
            )
            session.add(pelicula)


    def load_scores(self, df, session):
        for row in df.itertuples():
            score = Score(
                id = row[1],
                id_usuario = row[2],
                id_pelicula = row[3],
                puntuacion = row[4],
                fecha = row[5]
            )
            session.add(score)