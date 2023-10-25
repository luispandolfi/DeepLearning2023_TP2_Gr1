class Recommender:

    @classmethod
    def recomendar_peliculas(cls, id_usuario: int, k_peliculas: int):
        return {"id_usuario": id_usuario, "K": k_peliculas}
    
    @classmethod
    def peliculas_similares(cls, id_pelicula: int, k_peliculas: int):
        return {"id_pelicula": id_pelicula, "K": k_peliculas}