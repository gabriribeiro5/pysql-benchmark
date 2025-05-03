import random
import time
import logging

import aiomysql

from shared_use_cases.benchmark_async import AsyncBenchmark

import pdb


class AIOMySQLBench(AsyncBenchmark):
    async def run(self):
        # Create a connection pool using the specified pool class
        logging.info("creating connection pool")
        self.pool = await aiomysql.create_pool(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_KEY,
            db=self.DB_NAME,
            minsize=1,
            maxsize=self.num_batches,
            echo=True,
        )

        await self.async_create_table(self.pool)

        logging.info("Awaiting CRUD operations...")
        res = {
            "insert": await self.async_insert(self.pool),
            "select": await self.async_select(self.pool),
            "update": await self.async_update(self.pool),
            "delete": await self.async_delete(self.pool),
        }

        logging.info("AIOMySQLBench closing connection pool")
        self.pool.close()
        await self.pool.wait_closed()
        return res
