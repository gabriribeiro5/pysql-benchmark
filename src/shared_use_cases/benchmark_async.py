import asyncio
import random
import time
import logging
from utilities.logger import async_log_running_and_done
from bench_interfaces.benchmark_base import BenchmarkBase

import pdb


class AsyncBenchmark(BenchmarkBase):
    def __init__(self, num_batches=10):
        super().__init__()
        self.num_batches = num_batches  # Number of queries to run in parallel at once

    @async_log_running_and_done
    async def async_create_table(self, pool:isinstance):
        start_time = time.perf_counter()

        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                # Drop the table if it exists and create it again
                await cursor.execute(self.drop_table_query)
                await cursor.execute(self.create_table_query)
                await connection.commit()

        end_time = time.perf_counter()
        return end_time - start_time
    
    @async_log_running_and_done
    async def async_insert(self, pool:isinstance):
        start_time = time.perf_counter()

        async def async_insert_query(_):
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    # Insert sample data
                    data = f"Sample data {random.randint(1, 1000)}"
                    await cursor.execute(self.insert_query, (data,))
                    await connection.commit()

        await self._async_run_in_batches(async_insert_query)
        end_time = time.perf_counter()

        result = end_time - start_time

        if result == None:
            logging.error("Failed to calculate the execution time")
            raise Exception("Failed to calculate the execution time")
        else:
            return result

    @async_log_running_and_done
    async def async_select(self, *kwargs):
        start_time = time.perf_counter()

        async def async_select_query(i):
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(self.select_query, (i,))
                    await cursor.fetchone()

        await self._async_run_in_batches(async_select_query)

        end_time = time.perf_counter()
        return end_time - start_time

    @async_log_running_and_done
    async def async_update(self, *kwargs):
        start_time = time.perf_counter()

        async def async_update_query(i):
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    new_data = f"New data {random.randint(1, 1000)}"
                    await cursor.execute(self.update_query, (new_data, i))
                    await connection.commit()

        await self._async_run_in_batches(async_update_query)

        end_time = time.perf_counter()
        return end_time - start_time

    @async_log_running_and_done
    async def async_delete(self, *kwargs):
        start_time = time.perf_counter()

        async def async_delete_query(_):
            async with self.pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute(self.delete_query)
                    await connection.commit()
    
        await self._async_run_in_batches(async_delete_query)

        end_time = time.perf_counter()
        return end_time - start_time

    async def _async_run_in_batches(self, query_func):
        # Run queries in smaller batches
        for i in range(0, self.NUM_QUERIES, self.num_batches):
            # debugging_msg = f"Running batches {i+1} to {min(i + self.num_batches, self.NUM_QUERIES)}"
            batch = range(i + 1, min(i + self.num_batches + 1, self.NUM_QUERIES + 1))
            await asyncio.gather(*(query_func(j) for j in batch))
