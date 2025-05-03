import asyncio

import matplotlib.pyplot as plt # type: ignore
from connection_strategies.aiomysql_bench import AIOMySQLBench
from connection_strategies.asyncmy_bench import AsyncMyBench
from connection_strategies.mysqlclient_bench import MySQLdbBench
from connection_strategies.mysqlclient_threaded_bench import MySQLdbThreadedBench
from connection_strategies.pymysql_bench import PyMySQLBench
from connection_strategies.pymysql_threaded_bench import PyMySQLThreadedBench

from config import Definitions
from utilities.logger import LogSetup, log_running_and_done
import logging
import pdb
from time import time

class DBLibsBenchmark():
    def __init__(self):
        self.config = Definitions()
        if self.config.LOGGING_ENABLED:
                self.logger = LogSetup()
                self.logger.enableLog(self.config.LOG_DIR, self.config.LOG_FILE_NAME)

    def plot_histogram(self, data, libraries, queries):
        fig, ax = plt.subplots()

        # Create bar positions
        x = range(len(queries))
        total_width = 0.8  # Total width for all bars in a group
        width = total_width / len(libraries)  # Width of each bar
        
        logging.info("Ploting data for each library")
        # Plot data for each library
        for i, library in enumerate(libraries):
            # self.ensure_data(queries, data, library)
            times = []
            for query in queries:
                if data[library] == "skipped":
                    times.append(0)
                elif data[library] is not None and dict(data[library]).get(query) is not None:
                    times.append(dict(data[library]).get(query))
                else:
                    times.append(0)

            # times = [dict(data[library]).get(query) if data[library] is not None else 0 for query in queries] # Default to 0
            ax.bar([pos + i * width for pos in x], times, width, label=library)

        # Set labels and title
        logging.info("Setting labels and title")
        ax.set_xlabel("Queries")
        ax.set_ylabel("Time (seconds)")
        ax.set_title("Query Performance by Library")
        ax.set_xticks([pos + total_width / 2 for pos in x])
        ax.set_xticklabels(queries)

        # Add legend
        ax.legend()
        logging.info("Saving bench.png")
        plt.savefig("pysql_benchmark/bench.png")
        logging.info("Taking a nap")
        time.sleep(100000)

    
    def ensure_data(self, queries, data, library):
        for query in queries: # Ensure all query results exist in data
            try:
                if query not in data[library]:
                    msg = f"Missing data for {query} in {library}"
                    logging.warning(msg)
            except TypeError:
                msg = f"The {library}'s query ({query}) is probably None and is not iterable"
                logging.warning(msg)

    async def main(self):
        self.pymysql_bench = PyMySQLBench()
        self.pymysql_threaded_bench = PyMySQLThreadedBench()
        self.mysqlclient_bench = MySQLdbBench()
        self.mysqlclient_threaded_bench = MySQLdbThreadedBench()
        self.asyncmy_bench = AsyncMyBench()
        self.aiomysql_bench = AIOMySQLBench()

        # generate data dinamically using configuration variables
        logging.info("Starting lib executions...")
        data = {
            "PyMySQL": self.pymysql_bench.run() if self.config.USE_CASES_TO_RUN["pymysql"] else "skipped",
            "mysqlclient": self.mysqlclient_bench.run() if self.config.USE_CASES_TO_RUN["mysqlclient"] else "skipped",
            "PyMySQL T": self.pymysql_threaded_bench.run() if self.config.USE_CASES_TO_RUN["pymysql_t"] else "skipped",
            "mysqlclient T": self.mysqlclient_threaded_bench.run() if self.config.USE_CASES_TO_RUN["mysqlclient_t"] else "skipped",
            "aiomysql": await self.aiomysql_bench.run() if self.config.USE_CASES_TO_RUN["aiomysql"] else "skipped",
            "asyncmy": await self.asyncmy_bench.run() if self.config.USE_CASES_TO_RUN["asyncmy"] else "skipped",
        }

        logging.info("Finished runinng use cases")
        libraries = [lib for lib in data if lib != "skipped"]
        queries = ["insert", "select", "update", "delete"]
        self.plot_histogram(data, libraries, queries)


if __name__ == "__main__":
    bench = DBLibsBenchmark()
    asyncio.run(bench.main())
