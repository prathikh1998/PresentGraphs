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
redis_connection = redis.Redis.from_url("redis://quizredis.redis.cache.windows.net:6380?password=nkp3itVINJCqSXZDygXgqoo1baX48GwDTAzCaM4ZFX0=&ssl=True&abortConnect=False")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_queries', methods=['POST', 'GET'])
def random_queries():
    if request.method == 'POST':
        num_queries = int(request.form.get('num_queries'))

        query_results = []
        for _ in range(num_queries):
            # Generate a random query
            query = generate_random_query()

            # Check if the query result is already in Redis cache
            result = redis_connection.get(query)

            if result:
                # If the result is in cache, use it directly
                query_results.append((query, float(result)))
            else:
                # Execute the query
                start_time = time.time()
                cursor.execute(query)

                # Fetch the results (optional)
                results = cursor.fetchall()

                # Get the execution time
                query_time = time.time() - start_time

                # Store the query result in Redis cache
                redis_connection.set(query, query_time)

                query_results.append((query, query_time))

        return render_template('results.html', query_results=query_results)
    else:
        return render_template('random_queries.html')


@app.route('/restricted_queries', methods=['POST', 'GET'])
def restricted_queries():
    if request.method == 'POST':
        num_queries = int(request.form.get('num_queries'))

        query_results = []
        for _ in range(num_queries):
            # Generate a random restricted query
            query = generate_random_restricted_query()

            # Check if the query result is already in Redis cache
            result = redis_connection.get(query)

            if result:
                # If the result is in cache, use it directly
                query_results.append((query, float(result)))
            else:
                # Execute the query
                start_time = time.time()
                cursor.execute(query)

                # Fetch the results (optional)
                results = cursor.fetchall()

                # Get the execution time
                query_time = time.time() - start_time

                # Store the query result in Redis cache
                redis_connection.set(query, query_time)

                query_results.append((query, query_time))

        return render_template('results.html', query_results=query_results)
    else:
        return render_template('restricted_queries.html')


# Rest of the code...

if __name__ == '__main__':
    app.run()
