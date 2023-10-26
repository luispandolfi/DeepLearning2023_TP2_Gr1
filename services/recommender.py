from data.database_manager import DatabaseManager

class Recommender:

    singleton_instance = None

    @classmethod
    def get_instance(cls):
        if not cls.singleton_instance:
            cls.singleton_instance = Recommender()
        return cls.singleton_instance
    

    def __init__(self):
        self.databaseManager = DatabaseManager("postgresql://admin:Password01@127.0.0.1/sisrec")
    
    
    def recomendar_peliculas(self, id_usuario: int, k_peliculas: int):
        recomendadas = self.databaseManager.get_top_k_peliculas_rankeadas(k_peliculas, id_usuario)
        resultado = []
        for pelicula, puntaje in recomendadas:
            recomendada = {}
            recomendada['nombre'] = pelicula.nombre
            recomendada['fecha_estreno'] = pelicula.fecha_estreno
            recomendada['url'] = pelicula.url
            recomendada['puntaje'] = puntaje
            resultado.append(recomendada)
        return resultado
    

    def peliculas_similares(self, id_pelicula: int, k_peliculas: int):
        return {"id_pelicula": id_pelicula, "K": k_peliculas}