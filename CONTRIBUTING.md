# Testing and debugging

## Running the application with virtual environment:
If docker is not an option for you and you wish to run it with no virtualization, we recommend that you use a virtual environment.

For a complete experience with this project, we recommend you skip this section and go to the next one to run the app using docker-compose. Look for section "Runing the application iteractivelly with docker-compose".

### Windows
1. **Using CMD or PowerShell**, move to the projects directory and run:

```bash
    python3 -m venv .venv
```

2. If you are using **CMD**, move to `.venv\Scripts` and run:
```bash
    activate
```
Now skip to section 3.

2.1 If you are using **PowerShell**, you may need to unblock the activation script. Move to `.venv\Scripts` and run:
```bash
    Unblock-File -Path .\Activate.ps1
```

2.2 And set an Execution-Policy to your current user:
```bash
    Set-ExecutionPolicy -ExecutionPolicy AllSigned -Scope CurrentUser
```
This policy keeps you safe while from malicious scripts while allows the manually unblocked scripts.


2.3 Now you can run:
```bash
    .\Activate.ps1
```

3. After that you may install the required libraries.
Move back to the project's root directory and run:
```bash
    python3 -m pip install -r requirements.txt
```

4. To exit the virtual environment, simply run:
```bash
    deactivate
```

### WSL
Although:
1. Running a virtual environment in WSL is possible and
2. Connecting to MySQL from a subsystem is also possible (using special pluggins).
The tested libraries were not able to manage a connection from a subsystem (WSL) to an application (MySQL) hosted in the host system (Windows).

If you manage to make it work, please add up to this documentation and create a Pull Request.

But, given the reasons above, I recommend you to use Virtual Environment in your primary system (Windows).

### Linux
Move to the projects directory and run:

```bash
    python3 -m venv .venv
```

Then run:
```bash
    source .venv/bin/activate
```

After that you may install the required libraries.
Move back to the projects **root directory** and run:
```bash
    python3 -m pip install -r requirements.txt
```

### MacOS
- [ ] TODO

## Runing the application iteractivelly with docker-compose
First we must create a Docker image.
Open a terminal in the project root directory and run the following:
```bash
    docker build .
```

In order to access the container iteractive shell, you may choose between one of the following options:

1. **Use Docker-Compose to build (or rebuild) the image**
Open the **Docker Desktop** application.
Then open a terminal in the project root directory and execute:
```bash
    docker-compose up --build -d
```
Execute interactive commands using Docker Desktop

2. **Iteractively run a single container**
On a new terminal, run the following:
```bash
    docker run -p 80:80 -iteractive pysql_benchmark_image:latest
```

3. **Accessing Docker container after running it**
On a new terminal, run the following:
```bash
    docker exec -it <container_name> /bin/bash
```
Container names might be `pysql_bench_container_1` or `db_container_1`

### Talking to the applicationIn
Understand and manipulate the application using one (or a combination) of the following options:

1. **Reading logs**
All logs will be written to `/var/log/pysql_benchmark`.
Use the following command to read log updates in real time:
```bash
    tail -f /var/log/pysql_benchmark_/benchmark_.log
```

[Tip]: If docker-compose is being used, iteractive shell is not necessary.
Due to mount bindings on docker-compose.yml, you should be able to read from `./pysql-benchmark/logs/benchmark_.log` directly on your OS file system.

2. **Editing files**
- If you are running Docker Compose:
You can edit files directly in your code editor.
Changes made in the /src directory will be imediately applied to the container files.

- Otherwise:
By default, the docker image does not have any editor installed.
To apply any experimental change without having to rebuild the app,
Run the iteractive shell (option 1 or 2), and then run:
```bash
    apt update
    apt install vim
```

[Tip]: If docker-compose is being used, iteractive shell is not necessary.
Due to mount bindings on docker-compose.yml, you should be able to update files at `./src` directly on your OS file system.

