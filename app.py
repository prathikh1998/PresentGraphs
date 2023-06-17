import pyodbc
import random
import time
from flask import Flask, render_template, request

app = Flask(__name__)

# Azure SQL Database connection details
server = 'your_server.database.windows.net'
database = 'your_database'
username = 'your_username'
password = 'your_password'
driver = '{ODBC Driver 17 for SQL Server}'

# Create the connection string
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Route for random queries
@app.route('/random_queries', methods=['GET', 'POST'])
def random_queries():
    if request.method == 'POST':
        num_queries = int(request.form['num_queries'])
        
        # Connect to Azure SQL Database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Perform random queries
        query_results = []
        start_time = time.time()
        for _ in range(num_queries):
            # Generate a random ID for the query
            random_id = random.randint(1, 1000)

            # Execute the query
            query = f"SELECT * FROM Earthquakes WHERE id = {random_id}"
            cursor.execute(query)
            
            # Fetch the query result
            result = cursor.fetchone()
            query_results.append(result)

        # Calculate the time taken for queries
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Close the database connection
        cursor.close()
        conn.close()

        # Render the results template
        return render_template('results.html', query_type='Random Queries', results=query_results, elapsed_time=elapsed_time)

    return render_template('random_queries.html')

# Route for restricted queries
@app.route('/restricted_queries', methods=['GET', 'POST'])
def restricted_queries():
    if request.method == 'POST':
        # Retrieve the user's selection criteria
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        distance = int(request.form['distance'])

        # Connect to Azure SQL Database
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Perform restricted queries
        query_results = []
        start_time = time.time()

        # Execute the query
        query = f"SELECT * FROM Earthquakes WHERE geography::Point({latitude}, {longitude}, 4326).STDistance(geography::Point(latitude, longitude, 4326)) < {distance}"
        cursor.execute(query)

        # Fetch all query results
        results = cursor.fetchall()
        query_results.extend(results)

        # Calculate the time taken for the query
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Close the database connection
        cursor.close()
        conn.close()

        # Render the results template
        return render_template('results.html', query_type='Restricted Queries', results=query_results, elapsed_time=elapsed_time)

    return render_template('restricted_queries.html')

# Rest of your application code...

if __name__ == '__main__':
    app.run()
