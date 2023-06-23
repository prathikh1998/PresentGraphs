from flask import Flask, render_template, request, jsonify
import pyodbc

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
# Route for generating the chart based on user input
@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    attribute = request.form.get('attribute')
    interval = request.form.get('interval')

    min_val, max_val = interval.split('-')
    condition = f"{attribute} >= {min_val} AND {attribute} <= {max_val}"

    sql_query = f"""
        SELECT {attribute}_range, COUNT(*) AS count
        FROM (
            SELECT CASE
                WHEN {condition} THEN '{interval}'
                ELSE 'Other'
            END AS {attribute}_range
            FROM [city-1]
        ) AS subquery
        GROUP BY {attribute}_range
        ORDER BY
            CASE {attribute}_range
                WHEN '{interval}' THEN 1
                ELSE 99
            END
    """

    # Connect to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Execute the SQL query
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

     data = json.dumps(results)

    # Return the chart data as JSON
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()
