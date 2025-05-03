import random
import time
import logging

import MySQLdb

from shared_use_cases.benchmark import Benchmark


class MySQLdbBench(Benchmark):
    def _connect(self):
        logging.info("MySQLdbBench connecting")
        connection = MySQLdb.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_KEY,
            database=self.DB_NAME,
        )
        cursor = connection.cursor()
        return connection, cursor
