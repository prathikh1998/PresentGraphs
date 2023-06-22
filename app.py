from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

# Azure SQL Database connection settings
server = 'prathikhegde.database.windows.net'
database = 'ASSS2'
username = 'prathikhegde'
password = 'Tco7890$'
driver = '{ODBC Driver 17 for SQL Server}'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


@app.route('/chart', methods=['GET'])
def chart():
    return render_template('chart.html')

@app.route('/generate-chart', methods=['POST'])
def generate_chart():
    # Retrieve the form data and generate the chart
    data = request.form.get('data')
    chart_type = request.form.get('type')

    # Process the data and generate the chart using a suitable library (e.g., Matplotlib, Plotly, etc.)

    # Pass the chart data to index.html for display
    chart_data = ...  # Processed chart data

    return render_template('index.html', chart_data=chart_data)

@app.route('/query', methods=['POST'])
def execute_query():
    # Get the selected conditions from the form
    selected_conditions = request.form.getlist('condition')

    # Prepare the query based on the selected conditions
    query = "SELECT magnitude_range, quake_count FROM (SELECT CASE "

    for condition in selected_conditions:
        if condition == '1-2':
            query += "WHEN mag >= 1 AND mag < 2 THEN 'Magnitude 1-2' "
        elif condition == '2-3':
            query += "WHEN mag >= 2 AND mag < 3 THEN 'Magnitude 2-3' "
        elif condition == '3-4':
            query += "WHEN mag >= 3 AND mag < 4 THEN 'Magnitude 3-4' "
        elif condition == '4-5':
            query += "WHEN mag >= 4 AND mag <= 5 THEN 'Magnitude 4-5' "

    query += "ELSE 'Magnitude > 5' END AS magnitude_range, COUNT(*) AS quake_count FROM all_month "

    if selected_conditions:
        query += "WHERE " + " OR ".join(["(mag >= {} AND mag < {})".format(c.split('-')[0], c.split('-')[1]) for c in selected_conditions])

    query += " GROUP BY mag) AS subquery ORDER BY magnitude_range"

    try:
        # Execute the query and retrieve the results
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
    except pyodbc.Error as e:
        return f"An error occurred: {str(e)}"
        results = []

    # Render the results template with the query results
    return render_template('index.html', data=query, results=results)

if __name__ == '__main__':
    app.run(debug=True)
