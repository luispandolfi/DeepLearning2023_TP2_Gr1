from sqlalchemy import create_engine, select, func, delete
from sqlalchemy.orm import Session
from opensearchpy import Field, Boolean, Float, Integer, Document, Keyword, Text, DenseVector, Nested, Date, Object
from opensearchpy import OpenSearch
from data.data_frame_loader import DataFrameLoader
import numpy as np
import pandas as pd
import datetime


class DatavectorManager:

    def __init__(self, host, port, username, password):
        self.client = OpenSearch(host=host, port=port, auth=(username, password), http_auth =(username, password), use_ssl = True, verify_certs = False,)



    def load_Movies_Users_idx(self):
        dfs = DataFrameLoader.load_all("csv_files/personas.csv","csv_files/trabajadores.csv","csv_files/usuarios.csv","csv_files/peliculas.csv","csv_files/scores.csv")
        df_movies = dfs[3]
        df_users = dfs[2]
        movie_embeddings_matrix = np.load('./vectors/movie_embeddings_matrix.npy')
        user_embeddings_matrix = np.load('./vectors/user_embeddings_matrix.npy')
        user2Idx = np.load('./vectors/user2Idx.npy', allow_pickle=True).item()
        movie2Idx = np.load('./vectors/movie2Idx.npy', allow_pickle=True).item()
        print(f"movie_embeddings_matrix: {movie_embeddings_matrix.shape}")
        print(f"user_embeddings_matrix {user_embeddings_matrix.shape}")
        print(f"usee2Idx: {len(user2Idx)}")
        print(f"movie2Idx: {len(movie2Idx)}")

        df_users['userIdx'] = df_users['id'].apply(lambda x: user2Idx[x])
        df_movies['movieIdx'] = df_movies['id'].apply(lambda x: movie2Idx[x])
        return df_movies, df_users, movie_embeddings_matrix, user_embeddings_matrix, movie2Idx, user2Idx
    

    def load_Opensearch(self, df_peliculas_idx, df_usuarios_idx, movie_embeddings_matrix, user_embeddings_matrix, movieIdx, userIdx):

        method = {"name": "hnsw","space_type": "cosinesimil","engine": "nmslib"}

        class KNNVector(Field):
            name = "knn_vector"
            def __init__(self, dimension, method, **kwargs):
                super(KNNVector, self).__init__(dimension=dimension, method=method, **kwargs)

        index_name = 'movie'
        class Movie(Document):
            movie_id = Keyword()
            name = Text()
            release_date = Text()
            url = Text()
            action = Text() 
            adventure = Text()
            animation = Text()
            children = Text()
            comedy = Text()
            crime = Text()
            documentary = Text()
            drama = Text()
            fantasy = Text()
            film_noir = Text()
            horror = Text()
            musical = Text()
            mystery = Text()
            romance = Text()
            sci_fi = Text()
            thriller = Text()
            war = Text()
            western = Text()
            terror = Text()
            created_at = Date()

            vector = KNNVector(
                movie_embeddings_matrix.shape[1],
                method
            )
            class Index:
                name = index_name
                settings = {
                        'index': {
                        'knn': True
                    }
                }

            def save(self, ** kwargs):
                self.meta.id = self.movie_id
                return super(Movie, self).save(** kwargs)

        #Movie.init(using=self.client)
        try:
            self.client.indices.delete('movie')
        except Exception as e:
            print(str(e))


        print(self.client.indices.get(index="mo*"))


        for i , row in df_peliculas_idx.iterrows():
            #print(row['id'], row['Name'], row['Release Date'], row['IMDB URL'], (bool)(row['Action']), list(movie_embeddings_matrix[row.movieIdx]))
            if i < 1500:
                mv = Movie(
                    movie_id = row['id'],
                    name = row['Name'],
                    release_date = row['Release Date'],
                    url = row['IMDB URL'],
                    action =  row['Action'],
                    adventure = row['Adventure'],
                    animation = row['Animation'],
                    children = row["Children's"],
                    comedy = row['Comedy'],
                    crime = row['Crime'],
                    documentary = row['Documentary'],
                    drama = row['Drama'],
                    fantasy = row['Fantasy'],
                    film_noir = row['Film-Noir'],
                    horror = row['Horror'],
                    musical = row['Musical'],
                    mystery = row['Mystery'],
                    romance = row['Romance'],
                    sci_fi = row['Sci-Fi'],
                    thriller = row['Thriller'],
                    war = row['War'],
                    western = row['Western'],
                    created_at = datetime.datetime.now(),
                    vector = list(movie_embeddings_matrix[row.movieIdx])
                )
                mv.save(using=self.client)



    def listIndiceByName(self, id_pelicula, k_peliculas):
        #print(self.client.indices.get(index=str_busqueda))
        # Busco los valores cargados
        #df_movies, df_users, movie_embeddings_matrix, user_embeddings_matrix, movie2Idx, user2Idx = self.load_Movies_Users_idx()

        #Obtengo el vector de embedding para la pelicula solicitada
        response = self.client.search(index="movie", body={
                                                    "query": {
                                                        "match": {
                                                            "movie_id": id_pelicula
                                                        }
                                                    }
                                                })

        for h in response['hits']['hits']:
                #print(h['_source']['movie_id'], h['_source']['name'])
                movie_vector_embedding = h['_source']['vector']

        #Defino la query
        query = {
                    "size": k_peliculas + 1,
                    "query": {
                        "knn": {
                        "vector": {
                            "vector": movie_vector_embedding,
                            "k" : 10
                            }
                        }
                    }
                }
        #dictionary_response = {}
        list_response = []

        try:
            respuesta = self.client.search(body=query)
            for h in respuesta['hits']['hits']:
                #dictionary_response.update({"Nombre":h['_source']['movie_id'],"Id_movie": h['_source']['name']})
                list_response.append(h['_source']['name'])
                #print((str)(h['_source']['movie_id']), h['_source']['name'])
        except Exception as e:
            print(str(e))

        #return { "Nombre": h['_source']['name'], "Id_movie": h['_source']['movie_id']}
        return list_response






