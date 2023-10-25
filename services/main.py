from typing import Union
from fastapi import FastAPI
from recommender import Recommender

app = FastAPI()


@app.get("/peliculas/recomendar/{k_peliculas}/usuario/{id_usuario}")
def recomendar_peliculas(id_usuario: int, k_peliculas: int):
    return Recommender.recomendar_peliculas(id_usuario, k_peliculas)


@app.get("/peliculas/similares/{k_peliculas}/pelicula/{id_pelicula}")
def peliculas_similares(id_pelicula: int, k_peliculas: int):
    return Recommender.peliculas_similares(id_pelicula, k_peliculas)