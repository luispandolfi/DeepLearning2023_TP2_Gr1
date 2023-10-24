# %%
from opensearchpy import Field, Boolean, Float, Integer, Document, Keyword, Text, DenseVector, Nested, Date, Object
from opensearchpy import OpenSearch
import numpy as np
import pandas as pd
import datetime

# %%
header = ['userId', 'movieId', 'rating', 'timestamp']
df_movies = pd.read_csv('../ml-100k/u.item', sep='|', names=['id', 'name', 'fecha', 'x', 'url'] + list(range(19)) , encoding='latin-1')
df_users = pd.read_csv('../ml-100k/u.user', sep='|',  names=['id', 'age', 'ocupation', 'x'], encoding='latin-1')
# %%
df_movies.iloc[266]
# %%
df_movies.columns
# %%
movie_embeddings_matrix = np.load('../vectors/movie_embeddings_matrix.npy')
user_embeddings_matrix = np.load('../vectors/user_embeddings_matrix.npy')
user2Idx = np.load('../vectors/user2Idx.npy', allow_pickle=True).item()
movie2Idx = np.load('../vectors/movie2Idx.npy', allow_pickle=True).item()
# %%
movie2Idx
# %%
df_users['userIdx'] = df_users['id'].apply(lambda x: user2Idx[x])
df_movies['movieIdx'] = df_movies['id'].apply(lambda x: movie2Idx[x])
# %%
df_movies
# %%
df_movies.loc[df_movies['url'].isna(), 'url'] = ''
# %%
df_movies['url'].isna().sum()
# %%
movie_embeddings_matrix.shape[1]
# %%
host = 'localhost'
port = 9200
auth = ('admin', 'admin')

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_auth = auth,
    use_ssl = True,
    verify_certs = False,
)
# %%
client.cluster.health()
# %%
stats = client.
# %%
client.indices.delete('movie')
# %%
class KNNVector(Field):
    name = "knn_vector"
    def __init__(self, dimension, method, **kwargs):
        super(KNNVector, self).__init__(dimension=dimension, method=method, **kwargs)

method = {
    "name": "hnsw",
    "space_type": "cosinesimil",
    "engine": "nmslib"
}

# %%
index_name = 'movie'
class Movie(Document):
    movie_id = Keyword()
    url = Keyword()
    name = Text()
    created_at = Date()
    terror = Boolean()

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
# %%
# %%
Movie.init(using=client)
# %%
client.indices.get(index="*")
# %%
client.indices.exists('movie')

# %%
client.indices.get('movie')
# %%

# %%
df_movies.head(2)[1]
# %%
# %%
for i, row in df_movies.iterrows():
    mv = Movie(
        movie_id = row.id,
        url = row.url,
        name = row['name'],
        terror = row[0],
        vector = list(movie_embeddings_matrix[row.movieIdx]),
        creared_at = datetime.datetime.now()
    )
    mv.save(using=client)
# %%
row['name']
# %%
#    
mv = Movie(
        movie_id = row.id,
        url = row.url,
        name = row.name,
        terror = row[0],
        vector = list(movie_embeddings_matrix[row.movieIdx]),
        creared_at = datetime.datetime.now()
    ) 
# %%
mv.to_dict()
# %%
mv.save(using=client)
# %%
mv.meta.to_dict()
# %%
Movie.search(using=client).count()
# %%
movie_idx_to_search = 5

df_movies[df_movies['movieIdx'] == movie_idx_to_search]
# %%
movie_embeddings_matrix[movie_idx_to_search]
# %%
query = {
    "size": 5,
    "query": {
        "knn": {
        "vector": {
            "vector": movie_embeddings_matrix[movie_idx_to_search],
            "k" : 20
        }
        }
    }
}
# %%
response = client.search(index='movie', body=query)
# %%
for h in response['hits']['hits']:
    print(h)

# %%
