import MySQLdb
import logging

from shared_use_cases.benchmark_threaded import ThreadedBenchmark


class MySQLdbThreadedBench(ThreadedBenchmark):
    def _connect(self):
        logging.debug("MySQLdbThreadedBench connecting")
        connection = MySQLdb.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_KEY,
            database=self.DB_NAME,
        )
        cursor = connection.cursor()
        return connection, cursor
