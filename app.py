from flask import Flask, render_template, request
import random
import datetime
import time
import pyodbc
import redis

app = Flask(__name__)

# Connect to your Azure SQL database
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:prathikhegde.database.windows.net,1433;DATABASE=ASSS2;UID=prathikhegde;PWD=Tco7890$"
cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()

# Connect to your Azure Redis cache
redis_connection_string = "quizredis.redis.cache.windows.net:6380,password=nkp3itVINJCqSXZDygXgqoo1baX48GwDTAzCaM4ZFX0=,ssl=True,abortConnect=False"
redis_cache = redis.from_url(redis_connection_string)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_queries', methods=['POST', 'GET'])
def random_queries():
    if request.method == 'POST':
        num_queries = int(request.form.get('num_queries'))

        query_results = []
        for _ in range(num_queries):
            start_time = time.time()  # Start time for each query

            # Generate a random query
            query = generate_random_query()

            # Check if the result exists in the cache
            result = redis_cache.get(query)

            if result:
                # Result found in the cache
                query_time = "From Cache"
                result = eval(result)  # Convert the cached result from string to tuple
            else:
                # Execute the query
                cursor.execute(query)

                # Fetch the results (optional)
                results = cursor.fetchall()

                # Get the execution time
                query_time = time.time() - start_time

                # Store the result in the cache
                redis_cache.set(query, str((results, query_time)))  # Store the result as a string

            query_results.append((query, result))

        return render_template('results.html', query_results=query_results)
    else:
        return render_template('random_queries.html')


@app.route('/restricted_queries', methods=['POST', 'GET'])
def restricted_queries():
    if request.method == 'POST':
        num_queries = int(request.form.get('num_queries'))

        query_results = []
        for _ in range(num_queries):
            start_time = time.time()  # Start time for each query

            # Generate a random restricted query
            query = generate_random_restricted_query()

            # Check if the result exists in the cache
            result = redis_cache.get(query)

            if result:
                # Result found in the cache
                query_time = "From Cache"
                result = eval(result)  # Convert the cached result from string to tuple
            else:
                # Execute the query
                cursor.execute(query)

                # Fetch the results (optional)
                results = cursor.fetchall()

                # Get the execution time
                query_time = time.time() - start_time

                # Store the result in the cache
                redis_cache.set(query, str((results, query_time)))  # Store the result as a string

            query_results.append((query, result))

        return render_template('results.html', query_results=query_results)
    else:
        return render_template('restricted_queries.html')


def generate_random_query():
    table_name = "all_month"
    fields = [
        "time", "latitude", "longitude", "depth", "mag", "magType", "nst", "gap", "dmin", "rms",
        "net", "id", "updated", "place", "type", "horizontalError", "depthError", "magError",
        "magNst", "status", "locationSource", "magSource"
    ]

    # Generate a random query to fetch a random tuple
    random_field = random.choice(fields)
    query = f"SELECT TOP 1 {random_field} FROM {table_name} ORDER BY NEWID();"

    return query


def generate_random_restricted_query():
    table_name = "all_month"
    fields = [
        "time", "latitude", "longitude", "depth", "mag", "magType", "nst", "gap", "dmin", "rms",
        "net", "id", "updated", "place", "type", "horizontalError", "depthError", "magError",
        "magNst", "status", "locationSource", "magSource"
    ]

    # Generate a random restricted condition
    condition = generate_random_restricted_condition()

    # Generate a random query with the condition
    random_field = random.choice(fields)
    query = f"SELECT TOP 1 {random_field} FROM {table_name} WHERE {condition} ORDER BY NEWID();"

    return query


def generate_random_restricted_condition():
    conditions = [
        "place LIKE '%CA%'",
        f"time BETWEEN '{generate_random_date()}' AND '{generate_random_date()}'",
        f"mag BETWEEN {random.uniform(0, 10)} AND {random.uniform(0, 10)}"
    ]

    # Generate a random restricted condition
    condition = random.choice(conditions)

    return condition


def generate_random_date():
    # Generate a random date string between 2000-01-01 and 2023-12-31
    start_date = datetime.datetime(2000, 1, 1)
    end_date = datetime.datetime(2023, 12, 31)
    random_date = start_date + (end_date - start_date) * random.random()
    return random_date.strftime('%Y-%m-%d')


if __name__ == '__main__':
    app.run()
