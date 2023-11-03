from data.data_frame_loader import DataFrameLoader
from data.database_manager import DatabaseManager
from data.datavector_manager import DatavectorManager

class System:

    def __init__(self):
        self.db = DatabaseManager("postgresql://admin:Password01@127.0.0.1/sisrec")
        self.vector_db = DatavectorManager("localhost", 9200, "admin", "admin")
        dfs = DataFrameLoader.load_all("csv_files/personas.csv","csv_files/trabajadores.csv","csv_files/usuarios.csv","csv_files/peliculas.csv","csv_files/scores.csv")
        self.df_personas = dfs[0]
        self.df_trabajadores = dfs[1]
        self.df_usuarios = dfs[2]
        self.df_peliculas = dfs[3]
        self.df_scores = dfs[4]

    def setup_postgres_database(self):
        self.db.drop_tables()
        self.db.create_tables()
        self.db.load_initial_data(self.df_personas, self.df_trabajadores, self.df_usuarios, self.df_peliculas, self.df_scores)
    
    def update_predicted_scores(self):
        self.db.load_predicted_scores()
    
    def setup_vector_database(self):
        _, _, movie_embeddings_matrix, user_embeddings_matrix, movieIdx, userIdx = self.vector_db.load_Movies_Users_idx()
        self.vector_db.load_Opensearch(self.df_peliculas, self.df_usuarios, movie_embeddings_matrix, user_embeddings_matrix, movieIdx, userIdx)