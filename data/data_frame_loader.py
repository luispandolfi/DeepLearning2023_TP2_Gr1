import pandas as pd

class DataFrameLoader:
  
  @classmethod
  def load_all(cls, file_personas, file_trabajadores, file_usuarios, file_peliculas, file_scores):
    
    df_personas = cls.create_df_from_csv(file_personas)
    df_personas = cls.clean_df_personas(df_personas)

    df_trabajadores = cls.create_df_from_csv(file_trabajadores)
    df_trabajadores = cls.clean_df_trabajadores(df_trabajadores, df_personas)

    df_usuarios = cls.create_df_from_csv(file_usuarios)
    df_usuarios = cls.clean_df_usuarios(df_usuarios, df_personas)

    df_peliculas = cls.create_df_from_csv(file_peliculas)
    df_peliculas = cls.clean_df_peliculas(df_peliculas)

    df_scores = cls.create_df_from_csv(file_scores)
    df_scores = cls.clean_df_scores(df_scores, df_usuarios, df_peliculas)

    return df_personas, df_trabajadores, df_usuarios, df_peliculas, df_scores


  @classmethod
  def create_df_from_csv(cls, filename):
    df = pd.read_csv(filename)
    return df
  

  @classmethod
  def clean_df_personas(cls, df):
    df = df.dropna()
    df = df.drop_duplicates(subset = ["id"])
    df = df.loc[df["Gender"].isin(["M", "F"])]
    return df
  

  @classmethod
  def clean_df_trabajadores(cls, df, df_personas):
    df = df.dropna()
    df["Start Date"] = pd.to_datetime(df["Start Date"], format="%Y-%m-%d")
    id_personas = set(df_personas["id"])
    df = df.loc[df["id"].isin(id_personas)]
    return df
  

  @classmethod
  def clean_df_usuarios(cls, df, df_personas):
    df = df.dropna()
    df["Active Since"] = pd.to_datetime(df["Active Since"], format="%Y-%m-%d %H:%M:%S")
    id_personas = set(df_personas["id"])
    df = df.loc[df["id"].isin(id_personas)]
    return df
  
  
  @classmethod
  def clean_df_peliculas(cls, df):
    df = df.dropna(subset=['id', 'Name', 'Release Date', 'unknown', 'Action',
       'Adventure', 'Animation', "Children's", 'Comedy', 'Crime',
       'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
       'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])
    df["Release Date"] = pd.to_datetime(df["Release Date"], format="%d-%b-%Y")
    return df
  
  
  @classmethod
  def clean_df_scores(cls, df, df_usuarios, df_peliculas):
    df = df.dropna()
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")
    # el user_id exista en usuarios
    id_usuarios = set(df_usuarios["id"])
    df = df.loc[df["user_id"].isin(id_usuarios)]
    # el movie_id exista en peliculas
    id_peliculas = set(df_peliculas["id"])
    df = df.loc[df["movie_id"].isin(id_peliculas)]
    # rating entre 1 y 5
    df = df.loc[df["rating"].isin([1,2,3,4,5])]
    return df