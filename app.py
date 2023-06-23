from flask import Flask, render_template, request
import pyodbc
import json

app = Flask(__name__)

# Azure SQL Database connection settings
server = 'prathikhegde.database.windows.net'
database = 'ASSS2'
username = 'prathikhegde'
password = 'Tco7890$'
driver = '{ODBC Driver 17 for SQL Server}'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Route for displaying the chart configuration form
@app.route('/')
def chart_config():
    return render_template('chart.html')

# Route for generating the chart based on user input
@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    attribute = request.form.get('attribute')
    interval = request.form.get('interval')

    # Connect to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Execute the SQL query
    sql_query = f"SELECT population_range, COUNT(*) AS city_count FROM (SELECT CASE WHEN population >= 50000 AND population <= 100000 THEN 'Population 50000-100000' WHEN population > 100000 AND population <= 150000 THEN 'Population 100001-150000' WHEN population > 150000 AND population <= 200000 THEN 'Population 150001-200000' WHEN population > 200000 AND population <= 250000 THEN 'Population 200001-250000' ELSE 'Population > 250000' END AS population_range FROM [city-1]) AS subquery GROUP BY population_range ORDER BY CASE population_range WHEN 'Population 50000-100000' THEN 1 WHEN 'Population 100001-150000' THEN 2 WHEN 'Population 150001-200000' THEN 3 WHEN 'Population 200001-250000' THEN 4 ELSE 5 END"
    cursor.execute(sql_query)

    # Fetch all the rows
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    results = []
    for row in rows:
        result = {'attribute_value': row[0], 'count': row[1]}
        results.append(result)

    # Close the database connection
    cursor.close()
    conn.close()

    # Convert the results to JSON serializable format
    data = json.dumps(results)

    # Render the template with the data
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
