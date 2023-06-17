from flask import Flask, render_template, request
import time
import random

app = Flask(__name__)

# Function to simulate querying the earthquake data based on the specified parameters
# Function to establish a database connection
def connect_to_db():
    # Replace with your actual database connection details
    connection = pyodbc.connect(
        'Driver={ODBC Driver 18 for SQL Server};'
        'Server=tcp:prathikhegde.database.windows.net,1433;'
        'Database=ASSS2;'
        'Uid=prathikhegde;'
        'Pwd=Tco7890$;'
    )
    return connection

# Function to execute SQL queries
def execute_query(connection, query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result

def query_data(query_type, query_params):
    connection = connect_to_db()

    if query_type == 'random':
        num_queries = int(query_params['num_queries'])
        query_results = []
        for _ in range(num_queries):
            # SQL query to fetch random tuples from the all_month table
            query = "SELECT TOP 1 * FROM all_month ORDER BY NEWID()"
            result = execute_query(connection, query)
            query_results.append(result)
        connection.close()
        return query_results

    elif query_type == 'restricted':
        # Retrieve additional query parameters for restricted queries
        location = query_params['location']
        # Add more parameters as needed

        # SQL query to fetch restricted tuples from the all_month table
        query = f"SELECT * FROM all_month WHERE location = '{location}'"
        # Add more conditions to the query based on additional parameters

        result = execute_query(connection, query)
        connection.close()
        return result


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results.html', methods=['POST'])
def results():
    # Retrieve the query parameters from the form submission
    query_type = request.form.get('query-type')
    query_params = {}

    if query_type == 'random':
        query_params['num_queries'] = request.form.get('num-queries')
    elif query_type == 'restricted':
        # Retrieve additional query parameters for restricted queries
        # For example, latitude, longitude, time range, or magnitude range
        query_params['location'] = request.form.get('location')
        query_params['time_range'] = request.form.get('time-range')
        query_params['magnitude_range'] = request.form.get('magnitude-range')

    # Measure the time expended for executing the queries
    start_time = time.time()

    # Process the query parameters and execute the queries
    query_results = query_data(query_type, query_params)

    # Calculate the time expended
    elapsed_time = time.time() - start_time

    # Pass the results and elapsed time to the results.html template for rendering
    return render_template('results.html', query_results=query_results, elapsed_time=elapsed_time)

if __name__ == '__main__':
    app.run()
