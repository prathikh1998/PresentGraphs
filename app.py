from flask import Flask, render_template, request
import time
import random

app = Flask(__name__)

# Function to simulate querying the earthquake data based on the specified parameters
def query_data(query_type, query_params):
    # Simulating the execution of SQL queries
    # Replace with actual SQL queries to fetch data from the database
    
    if query_type == 'random':
        num_queries = int(query_params['num_queries'])
        query_results = []
        for _ in range(num_queries):
            # Simulating fetching random tuples from the dataset
            # Replace this with actual logic to retrieve random tuples
            query_results.append(f"Random Tuple: {random.randint(1, 1000)}")
        return query_results
    
    elif query_type == 'restricted':
        # Simulating fetching restricted tuples based on query parameters
        # Replace this with actual logic to retrieve restricted tuples
        return ['Restricted Tuple 1', 'Restricted Tuple 2', 'Restricted Tuple 3']

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
