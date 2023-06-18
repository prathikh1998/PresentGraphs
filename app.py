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
        query_results = []  # Initialize an empty list to store the query results

        start_time = time.time()
        for _ in range(num_queries):
            # Generate a random query
            query = generate_random_query()

            # Execute the query
            cursor.execute(query)

            # Fetch the results
            results = cursor.fetchall()

            # Append the query, results, and execution time to query_results
            query_results.append((query, results, time.time() - start_time))

        end_time = time.time()
        execution_time = end_time - start_time

        return render_template('results.html', num_queries=num_queries, execution_time=execution_time, query_results=query_results)
    else:
        return render_template('random_queries.html')



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


if __name__ == '__main__':
    app.run()
