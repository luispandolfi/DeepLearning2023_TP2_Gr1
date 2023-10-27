from data.database_manager import DatabaseManager

class Recommender:

    singleton_instance = None

    @classmethod
    def get_instance(cls):
        if not cls.singleton_instance:
            cls.singleton_instance = Recommender()
        return cls.singleton_instance
    

    def __init__(self):
        self.database_manager = DatabaseManager("postgresql://admin:Password01@127.0.0.1/sisrec")
    
    
    # Devuelve las k mejores recomendaciones de películas para el usuario dado.
    def recomendar_peliculas(self, id_usuario: int, k_peliculas: int):
        recomendadas = self.database_manager.get_top_k_peliculas_rankeadas(k_peliculas, id_usuario)
        resultado = []
        for pelicula, puntaje in recomendadas:
            recomendada = {}
            recomendada['id'] = pelicula.id
            recomendada['nombre'] = pelicula.nombre
            recomendada['fecha_estreno'] = pelicula.fecha_estreno
            recomendada['url'] = pelicula.url
            recomendada['puntaje'] = puntaje
            resultado.append(recomendada)
        return resultado
    

    # Devuelve las k películas más similares a la película dada.
    def peliculas_similares(self, id_pelicula: int, k_peliculas: int):
        #TODO hacerlo con knn llamando a la clase encargada de ello
        return {"id_pelicula": id_pelicula, "K": k_peliculas}
    

    # Para un usuario puntua una película, de esta forma se indica que el usuario vió la película.
    def puntuar_pelicula(self, id_usuario: int, id_pelicula: int, puntaje: int):
        error_message = self.database_manager.puntuar_pelicula(id_usuario, id_pelicula, puntaje)
        if error_message == None:
            return {"success": True}
        else:
            return { "success": False, "errorMessage": error_message}