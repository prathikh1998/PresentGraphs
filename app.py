@app.route('/random_queries', methods=['POST', 'GET'])
def random_queries():
    if request.method == 'POST':
        num_queries = int(request.form.get('num_queries'))

        start_time = time.time()
        for _ in range(num_queries):
            # Generate a random query
            query = generate_random_query()

            # Execute the query
            cursor.execute(query)

            # Fetch the results (optional)
            results = cursor.fetchall()

        end_time = time.time()
        execution_time = end_time - start_time

        return render_template('results.html', num_queries=num_queries, execution_time=execution_time)
    else:
        return render_template('random_queries.html')
