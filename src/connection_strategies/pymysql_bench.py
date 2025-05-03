import random
import time
import logging
import pymysql
from shared_use_cases.benchmark import Benchmark
import pdb

class PyMySQLBench(Benchmark):
    def _connect(self):
        connection = pymysql.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_KEY,
            database=self.DB_NAME,
        )
        cursor = connection.cursor()
        return connection, cursor
