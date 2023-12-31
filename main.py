from typing import Union
from fastapi import FastAPI
from services.recommender_service import Recommender

app = FastAPI()


@app.get("/peliculas/recomendar/{k_peliculas}/usuario/{id_usuario}")
def recomendar_peliculas(id_usuario: int, k_peliculas: int):
    return Recommender.get_instance().recomendar_peliculas(id_usuario, k_peliculas)


@app.get("/peliculas/similares/{k_peliculas}/pelicula/{id_pelicula}")
def peliculas_similares(id_pelicula: int, k_peliculas: int):
    return Recommender.get_instance().peliculas_similares(id_pelicula, k_peliculas)


@app.get("/usuario/{id_usuario}/pelicula/{id_pelicula}/puntuar/{puntaje}")
def puntuar_pelicula(id_usuario: int, id_pelicula: int, puntaje: int):
    return Recommender.get_instance().puntuar_pelicula(id_usuario, id_pelicula, puntaje)