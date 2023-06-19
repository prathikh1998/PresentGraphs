from flask import Flask, render_template, request
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

@app.route('/random_queries', methods=['POST', 'GET'])
def random_queries():
    if request.method == 'POST':
        num_queries = int(request.form.get('num_queries'))

        query_results = []
        start_time = time.time()
        for _ in range(num_queries):
            # Generate a random query
            query = generate_random_query()

            # Execute the query
            cursor.execute(query)

            # Fetch the results (optional)
            results = cursor.fetchall()

            # Get the execution time
            query_time = time.time() - start_time

            query_results.append((query, query_time))

        return render_template('results.html', query_results=query_results)
    else:
        return render_template('random_queries.html')


@app.route('/restricted_queries', methods=['GET'])
def restricted_queries():
    return render_template('restricted_queries.html')


@app.route('/restricted_results', methods=['POST'])
def restricted_results():
    location = request.form.get('location')
    distance = float(request.form.get('distance'))
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    min_magnitude = float(request.form.get('min_magnitude'))
    max_magnitude = float(request.form.get('max_magnitude'))

    query_results = []

    # Generate a random query based on the specified conditions
    query = generate_restricted_query(location, distance, start_time, end_time, min_magnitude, max_magnitude)

    # Execute the query
    cursor.execute(query)

    # Fetch the results (optional)
    results = cursor.fetchall()

    # Get the execution time
    query_time = time.time() - start_time

    query_results.append((query, query_time))

    return render_template('results.html', query_results=query_results)


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


def generate_restricted_query(location, distance, start_time, end_time, min_magnitude, max_magnitude):
    # Generate a query based on the specified conditions
    query = f"SELECT * FROM all_month WHERE location = '{location}' AND distance < {distance} AND time BETWEEN '{start_time}' AND '{end_time}' AND mag BETWEEN {min_magnitude} AND {max_magnitude}"

    return query


if __name__ == '__main__':
    app.run()
