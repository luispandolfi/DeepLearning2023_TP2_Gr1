from keras.models import Model, load_model
import numpy as np

class RecommenderModel:

    def __init__(self, model_file_path, user2Idx_file_path, movie2idx_file_path):
        self.model = load_model(model_file_path)
        self.user2Idx = np.load(user2Idx_file_path, allow_pickle=True).item() # item() is needed to convert the nparray to a dict
        self.movie2Idx = np.load(movie2idx_file_path, allow_pickle=True).item()
    

    # user_id: int
    # movie_id: int
    # movie_genre_list: list of int / length 18
    def predict_score(self, user_id, movie_id, movie_genre_list):

        # map the ids to the indexes used in the model
        userIdx = self.user2Idx[user_id]
        movieIdx = self.movie2Idx[movie_id]

        # build the input values
        user_input = np.array([userIdx])
        movie_input = np.array([movieIdx])
        genre_input = np.array([movie_genre_list])

        # predict
        return self.model.predict([user_input, movie_input, genre_input])