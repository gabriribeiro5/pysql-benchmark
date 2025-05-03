# Use a base Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /src

# Set desired timezone (ref: https://dev.to/bitecode/set-timezone-in-your-docker-image-d22)
RUN apt install tzdata -y
ENV TZ="America/Sao_Paulo"

# Copy setup_mysql_env script file
COPY setup_mysql_env.sh /src

# Set permissions for setup_mysql_env
RUN chmod +x setup_mysql_env.sh

# Run setup_mysql_env script
RUN bash setup_mysql_env.sh

# Create application's directory
RUN mkdir pysql_benchmark

# Copy requirements file
COPY ./src/requirements.txt /src/pysql_benchmark

# Install dependencies
RUN python -m pip install --no-cache-dir -r /src/pysql_benchmark/requirements.txt

# Copy the rest of the app code
COPY ./src /src/pysql_benchmark

# Set PYTHONPATH to the app directories
ENV PYTHONPATH="/src:/src/pysql_benchmark"

# Expose the default port
# EXPOSE 3306

# Run application
# RUN python3 pysql_benchmark/main.py

# Start the application
ENTRYPOINT ["sh", "-c", "python3 pysql_benchmark/main.py || bash"]

