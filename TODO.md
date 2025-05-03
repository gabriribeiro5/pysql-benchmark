# **TODO List**
A list of improvement sugestions.

## Documentation
- [x] Create TODO list to log improvements in this benchmark
- [x] CONTRIRBUTING.md file: for developers who wish to improve this project

## Virtual Environment
- [ ] Include troubleshooting information at CONTRIBUTING.md
  - [x] Windows CMD
  - [x] Windows PowerShell
  - [x] Windows WSL
  - [x] Linux
  - [ ] MacOS

## Design
- [x] Organize source files into 3 directories: `bench_interface`, `connection_strategies` and `shared_use_cases`
- [x] Fix importing errors
- [x] Create `utilities` directory to attach logging features

## New features
- [x] `.gitignore` for python applications
- [x] Configuration file: to centrilize and define application details such as database parameters, which connection strategies the app should run, whether the logging feature must be enabled or not, etc...
- [x] Logging utility: lightweight and helpful for debugging :slightly_smiling_face:. More details in `utils/logger.py` file's docstrings.

## Refactoring
- [x] (main.py): Move methods `plot_histogram` and `main` into new class (QueryPerformance), for better integration with the features above
- [x] (benchmark_threaded.py): Meaningful method names (on ThreadedBenchmark, use `t_insert` instead of `insert`)
- [x] (multiple files): Implement logging decorator over all methods
- [x] (multiple files): Upgrade time counter from `time.time()` to `time.perf_counter()`, for greater accuracy.

## Infrastructure
- [x] Containerize application (**dockerfile**): Enabling resource restrictions setup and improving real use case simulation.
  - [x] get python image
  - [x] add shell script to automate environment setup for `mysqlclient` lib
  - [x] install requirements.txt
  - [x] set PYTHONPATH
  - [x] start application
- [x] Automate container orchesration (**docker-compose**): Enabling an easy debugging process and execution of multiple containers.

## Debugging
- [x] fix(multiple files): typos from the Refactoring phase (above). Tears and sweat were shed here.
- [x] fix(aiomysql_bench.py): Add a call to the method `async_create_table()` to match `aiomysql_bench`'s and `asyncmy_bench`'s `run()` behavior.

## Database docker
- [x] Containerize database: Automate db setup.
- [ ] Stablish connection through docker-compose secrets (remove db details from config file).

## pysql_bench docker image
- [ ] Move shell script content to Dockerfile
- [ ] Publish docker image

## Application logic
- [ ] Implement 1 connection per task/thread: make sure every task has its own connection.
-> Explanation: In the current scenario, we are considering that our application is meant to first gather plenty of data and, only then, insert all of it in our database at once. That may apply for data migration, backup or CRUD operations but not for a REST API (a farly common use case for such libraries).
In a REST API, each db operation represents a unique request, therefore, every task should be self-sufficient, otherwise a single connection would be forever open for every type of request. That means being able to:
  1. Proccess the request file,
  2. Connect to DB,
  3. Apply some DML,
  4. Return a response to the requester.
  (All in one task).
  **Though tasks 1 and 4 are not applicable in this benchmark, tasks 2 and 3 are included.**

- [ ] One container per library: the required docker-compose syntax is already defined in the file comments (search: api2)
-> Explanation: Once every operation type (INSERT, SELECT, UPDATE and DELETE) starts right after the previous one (and once those operations are heavy loaded), I suspect that some of those tasks may be impacting hardware performance while new tasks have already started.
After each task finishes, all coroutines are discarted, supose ASYNCMY executes many coroutines: after the last coroutine returns its value, the next operation is alowed to run but it doesn't mean the coroutine cleanup operation is finished. If this is correct, then one library's operations might be sharing computaional resources with clean up operations from the previous one.
Once we don't know how long the interpreter takes to execute underling tasks such as coroutines cleanup, having each library isoleted in one container, might help us understand (and be more fair with) each library behaviour, regardless any other lib that may have been executed previously in the same environment.