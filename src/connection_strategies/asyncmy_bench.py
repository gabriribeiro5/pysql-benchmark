import asyncio
import random
import time
from asyncio import Queue
import logging

import asyncmy

from shared_use_cases.benchmark_async import AsyncBenchmark


class AsyncMyBench(AsyncBenchmark):
    async def run(self):
        # Create a connection pool manually
        logging.info("creating connection pool")
        self.pool = await asyncmy.create_pool(
            host=self.DB_HOST,
            user=self.DB_USER,
            password=self.DB_KEY,
            db=self.DB_NAME,
            maxsize=self.num_batches,
        )

        await self.async_create_table(self.pool)
        logging.info("Awaiting CRUD operations...")
        res = {
            "insert": await self.async_insert(self.pool),
            "select": await self.async_select(self.pool),
            "update": await self.async_update(self.pool),
            "delete": await self.async_delete(self.pool),
        }

        logging.info("AsyncMyBench closing connection pool")
        self.pool.close()
        await self.pool.wait_closed()
        return res
