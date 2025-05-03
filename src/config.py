from pathlib import Path

class Definitions():
    def __init__(self):
        ### BASE DIRECTORIES ###
        self.SRC_DIR = Path(__file__).resolve().parent.parent
        self.LOG_DIR = "/var/log/pysql_benchmark"
        self.LOG_FILE_NAME = "benchmark"

        ### APPLICATION CONFIGURATION ###
        self.LOGGING_ENABLED = True
        self.USE_CASES_TO_RUN = {
            "pymysql": True,
            "mysqlclient": True,
            "pymysql_t": True,
            "mysqlclient_t": True,
            "aiomysql": True,
            "asyncmy": True,
        }

        ### DATABASE INFORMATION ### 
        self.DB_CONN = "pysql_benchmark"
        self.DB_NAME = "py_bench_db"
        self.DB_HOST = "mysql"
        self.DB_PORT = 3306
        self.DB_USER = "root"
        self.DB_KEY = "pwd123"
        self.NUM_QUERIES = 10000