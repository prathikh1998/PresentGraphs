from flask import Flask, render_template, request
import random
import datetime
import time
import pyodbc
import redis
import json

app = Flask(__name__)
cache = redis.Redis(host='quizredis.redis.cache.windows.net', port=6380, password='ynkp3itVINJCqSXZDygXgqoo1baX48GwDTAzCaM4ZFX0=', ssl=True)

# Connect to your Azure SQL database
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:prathikhegde.database.windows.net,1433;DATABASE=ASSS2;UID=prathikhegde;PWD=Tco7890$"
cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/random_queries', methods=['POST', 'GET'])
def random_queries():
    try:
        if request.method == 'POST':
            num_queries = int(request.form.get('num_queries'))

            query_results = []
            total_time = 0  # Initialize total time

            for _ in range(num_queries):
                # Generate a random query
                query = generate_random_query()

                # Check if the result is cached
                start_time = time.time()  # Start the timer
                result = fetch_results_from_cache(query)
                query_time = time.time() - start_time

                if result is None:
                    # Execute the query and fetch the results
                    start_time = time.time()  # Start the timer
                    cursor.execute(query)
                    results = cursor.fetchall()

                    # Convert the pyodbc.Row objects to dictionaries
                    rows = []
                    for row in results:
                        row_dict = {}
                        for idx, column in enumerate(cursor.description):
                            row_dict[column[0]] = row[idx]
                        rows.append(row_dict)

                    # Get the execution time
                    query_time += time.time() - start_time
                    total_time += query_time  # Add query time to the total

                    query_results.append((query, query_time, rows))

                    # Cache the results
                    cache_results(query, rows)
                else:
                    # Use the cached results
                    query_results.append((query, query_time, result))

            return render_template('results.html', query_results=query_results, total_time=total_time)
        else:
            return render_template('random_queries.html')
    except Exception as e:
        # Log the exception
        app.logger.exception(e)

@app.route('/restricted_queries', methods=['POST', 'GET'])
def restricted_queries():
    if request.method == 'POST':
        num_queries = int(request.form.get('num_queries'))

        query_results = []
        total_time = 0  # Initialize total time

        for _ in range(num_queries):
            # Generate a random restricted query
            query = generate_random_restricted_query()

            # Check if the result is cached
            start_time = time.time()  # Start the timer
            result = fetch_results_from_cache(query)
            query_time = time.time() - start_time

            if result is None:
                # Execute the query and fetch the results
                start_time = time.time()  # Start the timer
                cursor.execute(query)
                results = cursor.fetchall()

                # Convert the pyodbc.Row objects to dictionaries
                rows = []
                for row in results:
                    row_dict = {}
                    for idx, column in enumerate(cursor.description):
                        row_dict[column[0]] = row[idx]
                    rows.append(row_dict)

                # Get the execution time
                query_time += time.time() - start_time
                total_time += query_time  # Add query time to the total

                query_results.append((query, query_time, rows))

                # Cache the results
                cache_results(query, rows)
            else:
                # Use the cached results
                query_results.append((query, query_time, result))

        return render_template('results.html', query_results=query_results, total_time=total_time)
    else:
        return render_template('restricted_queries.html')


def fetch_results_from_cache(query):
    # Check if the query result is cached
    result = cache.get(query)

    if result is not None:
        # Decode the cached result and return it
        return json.loads(result)

    return None

def cache_results(query, result):
    # Convert the result to a JSON string before caching
    cache.set(query, json.dumps(result))

def generate_random_query():
    table_name = "all_month"
    fields = [
        "time", "latitude", "longitude", "depth", "mag", "magType", "nst", "gap", "dmin", "rms",
        "net", "id", "updated", "place", "type", "horizontalError", "depthError", "magError",
        "magNst", "status", "locationSource", "magSource"
    ]

    # Generate a random query to fetch a random tuple
    random_field = random.choice(fields)
    query = f"SELECT TOP 10 {random_field} from {table_name} ORDER BY NEWID();"

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
    query = f"SELECT TOP 10 {random_field} FROM {table_name} WHERE {condition} ORDER BY NEWID();"

    return query


def generate_random_restricted_condition():
    conditions = [
        "place LIKE '%California%'",
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
