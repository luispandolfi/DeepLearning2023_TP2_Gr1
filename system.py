from data.database_manager import DatabaseManager

class System:

    db = DatabaseManager("postgresql://admin:Password01@127.0.0.1/sisrec")
    
    @classmethod
    def setup_postgres_database(cls):
        cls.db.drop_tables()
        cls.db.create_tables()
        cls.db.load_initial_data()
    
    @classmethod
    def update_predicted_scores(cls):
        cls.db.load_predicted_scores()