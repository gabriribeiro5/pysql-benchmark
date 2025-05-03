from config import Definitions

class BenchmarkBase(Definitions):
    def __init__(self) -> None:
        config = Definitions()
        self.DB_HOST = config.DB_HOST
        self.DB_PORT = config.DB_PORT
        self.DB_USER = config.DB_USER
        self.DB_KEY = config.DB_KEY
        self.DB_NAME = config.DB_NAME
        self.NUM_QUERIES = config.NUM_QUERIES

        self.create_table_query = """
        CREATE TABLE IF NOT EXISTS test_table (
            id INT AUTO_INCREMENT PRIMARY KEY,
            data VARCHAR(100)
        )
        """
        self.drop_table_query = "DROP TABLE IF EXISTS test_table"

        self.insert_query = "INSERT INTO test_table (data) VALUES (%s)"
        self.select_query = "SELECT * FROM test_table WHERE id = %s"
        self.delete_query = "DELETE FROM test_table WHERE 1 LIMIT 1"
        self.update_query = "UPDATE test_table SET data = %s WHERE id = %s"

    def _connect():
        raise NotImplementedError()
