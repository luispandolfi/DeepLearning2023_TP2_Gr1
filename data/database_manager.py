from sqlalchemy import create_engine, inspect, select, func, delete
from sqlalchemy.orm import Session
from model.base_model import BaseModel
from model.persona import Persona
from model.usuario import Usuario
from model.trabajador import Trabajador
from model.pelicula import Pelicula
from model.score import Score
from model.prediccion_score import PrediccionScore
from datetime import date
from services.recommender_model import RecommenderModel


class DatabaseManager:

    def __init__(self, connectionString):
        self.engine = create_engine(connectionString) #agregar echo=True param para debug


    def drop_tables(self):
        for table in BaseModel.metadata.sorted_tables:
            self.__drop_table(table)
    

    def __drop_table(self, table):
        if inspect(self.engine).has_table(table.name):
            table.drop(self.engine)


    def create_tables(self):
        BaseModel.metadata.create_all(self.engine)


    def load_initial_data(self, df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores):
        with Session(self.engine) as session:
            self.load_personas(df_personas, session)
            self.load_trabajadores(df_trabajadores, session)
            self.load_usuarios(df_usuarios, session)
            self.load_peliculas(df_peliculas, session)
            self.load_scores(df_scores, session)
            session.commit()


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
    

    # Devuelve para un usuario las k películas con mayor puntaje predicto, ordenadas por puntaje de mayor a menor.
    # Éstas son películas que el usuario no ha vista, ya que se almacenan las predicciones únicamente para las películas no vistas.
    def get_top_k_peliculas_rankeadas(self, k, id_usuario):
        stmt = select(Pelicula, PrediccionScore.puntuacion) \
            .where(PrediccionScore.id_usuario == id_usuario) \
            .where(Pelicula.id == PrediccionScore.id_pelicula) \
            .order_by(PrediccionScore.puntuacion.desc()).limit(k)        
        with Session(self.engine) as session:
            return session.execute(stmt).all()
    

    # Al puntuar una película la estamos marcando como ya vista.
    # Este método:
    # - agrega o actualiza el puntaje en Scores
    # - elimina la predicción en PrediccionesScore
    # En caso de error devuelve un mensaje correspondiente, sino devuelve None.
    def puntuar_pelicula(self, id_usuario, id_pelicula, puntaje):
        if puntaje < 1 or puntaje > 5:
            return "El puntaje debe estar entre 1 y 5"
        
        try:
            with Session(self.engine) as session:
                # agrego/actualizo Scores
                score = self.__get_score(session, id_usuario, id_pelicula)
                if score == None:
                    # el score no existe, entonces lo inserto
                    maxId = session.scalar(select(func.max(Score.id))) #TODO evitar mediante un autogenerado en la base de datos
                    fecha_hoy = date.today().strftime("%Y-%m-%d") #TODO habria que cambiar para recibir un objeto fecha
                    score = Score(id_usuario, id_pelicula, puntaje, fecha_hoy, id=maxId+1)
                else:
                    # el score ya existe, entonces le actualizo el puntaje
                    score.puntuacion = puntaje
                session.add(score)

                # elimino de PrediccionesScore
                session.execute(delete(PrediccionScore) \
                                .where(PrediccionScore.id_usuario == id_usuario) \
                                .where(PrediccionScore.id_pelicula == id_pelicula))
                
                # commit de cambios
                session.commit()
                return None
        except:
            return "Ha ocurrido un error."
    

    def __get_score(self, session: Session, id_usuario, id_pelicula):
        return session.scalar(
            select(Score) \
            .where(Score.id_usuario == id_usuario) \
            .where(Score.id_pelicula == id_pelicula))
    

    def load_predicted_scores(self):
        model = RecommenderModel('vectors/model.keras', 'vectors/user2Idx.npy', 'vectors/movie2Idx.npy')
        with Session(self.engine) as session:
            # elimina predicciones anteriores
            session.execute(delete(PrediccionScore))
            # para todos los usuarios
            for user in session.execute(select(Usuario)):
                user_id = user[0].id
                print(f'Prediciendo para usuario : {user_id} ...')
                user_batch = []
                movie_batch = []
                genres_batch = []
                # consulta las peliculas que el usario aun no ha visto (no ha puntuado)
                not_seen_movies = select(Pelicula).where(Pelicula.id.not_in(
                    select(Score.id_pelicula).where(Score.id_usuario == user_id)
                ))
                for movie in session.execute(not_seen_movies):
                    movie_id = movie[0].id
                    movie_genres = movie[0].get_genres()    
                    # agrega el usuario y pelicula al batch
                    user_batch = user_batch + [user_id]
                    movie_batch = movie_batch + [movie_id]
                    genres_batch = genres_batch + [movie_genres]
                # predice y actualiza el batch
                self.__predict_and_update_score(session, model, user_batch, movie_batch, genres_batch)
            # confirma cambios
            session.commit()
    

    def __predict_and_update_score(self, session, model, users, movies, movies_genres):
        model_result = model.batch_predict_score(users, movies, movies_genres)
        for i, user_id in enumerate(users):
            movie_id = movies[i]
            score = float(model_result[i][0])
            predicted_score = PrediccionScore(user_id, movie_id, score)
            session.add(predicted_score)