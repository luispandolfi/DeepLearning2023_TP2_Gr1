from data.database_manager import DatabaseManager
from data.datavector_manager import DatavectorManager 

class Recommender:

    singleton_instance = None

    @classmethod
    def get_instance(cls):
        if not cls.singleton_instance:
            cls.singleton_instance = Recommender()
        return cls.singleton_instance
    

    def __init__(self):
        self.databaseManager = DatabaseManager("postgresql://admin:Password01@127.0.0.1/sisrec")
        self.datavectorManager = DatavectorManager("localhost", 9200, "admin" , "admin")
    
    
    # Devuelve las k mejores recomendaciones de películas para el usuario dado.
    def recomendar_peliculas(self, id_usuario: int, k_peliculas: int):
        recomendadas = self.databaseManager.get_top_k_peliculas_rankeadas(k_peliculas, id_usuario)
        resultado = []
        for pelicula, puntaje in recomendadas:
            recomendada = {}
            recomendada['id'] = pelicula.id
            recomendada['nombre'] = pelicula.nombre
            recomendada['fecha_estreno'] = pelicula.fecha_estreno
            recomendada['url'] = pelicula.url
            recomendada['puntaje'] = puntaje
            recomendada['generos'] = pelicula.get_genres_as_string_list()
            resultado.append(recomendada)
        return resultado
    

    # Devuelve las k películas más similares a la película dada.
    def peliculas_similares(self, id_pelicula: int, k_peliculas: int):
        recomendadas = self.datavectorManager.listIndiceByName(id_pelicula, k_peliculas)
        return recomendadas
    

    # Para un usuario puntua una película, de esta forma se indica que el usuario vió la película.
    def puntuar_pelicula(self, id_usuario: int, id_pelicula: int, puntaje: int):
        error_message = self.databaseManager.puntuar_pelicula(id_usuario, id_pelicula, puntaje)
        if error_message == None:
            return {"success": True}
        else:
            return { "success": False, "errorMessage": error_message}