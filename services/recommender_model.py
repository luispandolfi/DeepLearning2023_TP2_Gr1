from keras.models import Model, load_model
import numpy as np

class RecommenderModel:

    def __init__(self, model_file_path, user2Idx_file_path, movie2idx_file_path):
        self.model = load_model(model_file_path)
        self.user2Idx = np.load(user2Idx_file_path, allow_pickle=True).item() # item() is needed to convert the nparray to a dict
        self.movie2Idx = np.load(movie2idx_file_path, allow_pickle=True).item()
    

    # users: list of in
    # movies: list of int
    # movie_genres: list of genres - genres is a 18 items list (an item is a 0 or 1)
    def batch_predict_score(self, users, movies, movie_genres):

        # map the ids to the indexes used in the model
        userIdx = [self.user2Idx[x] for x in users]
        movieIdx = [self.movie2Idx[x] for x in movies]

        # build the input values
        user_input = np.array(userIdx)
        movie_input = np.array(movieIdx)
        movie_genres_input = np.array(movie_genres)

        # predict
        return self.model.predict([user_input, movie_input, movie_genres_input])