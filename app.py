from flask import Flask, render_template, request, redirect, url_for
import random
import time
import pyodbc

app = Flask(__name__)

# Connect to your Azure SQL database
connection_string = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:prathikhegde.database.windows.net,1433;DATABASE=ASSS2;UID=prathikhegde;PWD=Tco7890$"
cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_queries', methods=['POST'])
def random_queries():
    if request.method == 'POST':
        num_queries = int(request.form.get('num_queries'))

        query_results = []
        for _ in range(num_queries):
            # Generate a random query
            query = generate_random_query()

            # Execute the query
            start_time = time.time()
            cursor.execute(query)
            end_time = time.time()

            # Calculate the execution time
            execution_time = end_time - start_time

            # Append the query and execution time to the results list
            query_results.append((query, execution_time))

        return render_template('results.html', num_queries=num_queries, query_results=query_results)

@app.route('/restricted_queries')
def restricted_queries():
    return render_template('restricted_queries.html')

@app.route('/generate_restricted_queries', methods=['POST'])
def generate_restricted_queries():
    if request.method == 'POST':
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        min_magnitude = float(request.form.get('min_magnitude'))
        max_magnitude = float(request.form.get('max_magnitude'))
        num_queries = int(request.form.get('num_queries'))

        query_results = []
        for _ in range(num_queries):
            # Generate a restricted query
            query = generate_restricted_query(latitude, longitude, start_date, end_date, min_magnitude, max_magnitude)

            # Execute the query
            start_time = time.time()
            cursor.execute(query)
            end_time = time.time()

            # Calculate the execution time
            execution_time = end_time - start_time

            # Append the query and execution time to the results list
            query_results.append((query, execution_time))

        return render_template('results.html', num_queries=num_queries, query_results=query_results)

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


def generate_restricted_query(latitude, longitude, start_date, end_date, min_magnitude, max_magnitude):
    table_name = "all_month"
    fields = [
        "time", "latitude", "longitude", "depth", "mag", "magType", "nst", "gap", "dmin", "rms",
        "net", "id", "updated", "place", "type", "horizontalError", "depthError", "magError",
        "magNst", "status", "locationSource", "magSource"
    ]

    # Generate a restricted query based on the specified restrictions
    random_field = random.choice(fields)
    query = f"SELECT TOP 1 {random_field} FROM {table_name} WHERE latitude = {latitude} AND longitude = {longitude} AND time BETWEEN '{start_date}' AND '{end_date}' AND mag BETWEEN {min_magnitude} AND {max_magnitude} ORDER BY NEWID();"

    return query


if __name__ == '__main__':
    app.run()
