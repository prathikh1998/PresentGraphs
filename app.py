from flask import Flask, render_template
import pyodbc
import json

app = Flask(__name__)

# Azure SQL Database connection settings
server = 'prathikhegde.database.windows.net'
database = 'ASSS2'
username = 'prathikhegde'
password = 'Tco7890$'
driver = '{ODBC Driver 17 for SQL Server}'

# Route for displaying the chart in HTML
@app.route('/')
def display_chart():
    # Connect to Azure SQL Database
    connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"
    conn = pyodbc.connect(connection_string)

    # Execute the query
    query = """
        SELECT
            magnitude_range,
            COUNT(*) AS quake_count
        FROM (
            SELECT
                CASE
                    WHEN mag < 1 THEN 'Magnitude < 1'
                    WHEN mag >= 1 AND mag < 2 THEN 'Magnitude 1-2'
                    WHEN mag >= 2 AND mag < 3 THEN 'Magnitude 2-3'
                    WHEN mag >= 3 AND mag < 4 THEN 'Magnitude 3-4'
                    WHEN mag >= 4 AND mag <= 5 THEN 'Magnitude 4-5'
                    ELSE 'Magnitude > 5'
                END AS magnitude_range
            FROM
                all_month
        ) AS subquery
        GROUP BY
            magnitude_range
        ORDER BY
            CASE magnitude_range
                WHEN 'Magnitude < 1' THEN 1
                WHEN 'Magnitude 1-2' THEN 2
                WHEN 'Magnitude 2-3' THEN 3
                WHEN 'Magnitude 3-4' THEN 4
                WHEN 'Magnitude 4-5' THEN 5
                ELSE 6
            END
    """

    cursor = conn.cursor()
    cursor.execute(query)

    # Fetch the query results
    results = cursor.fetchall()

    # Convert the results to JSON format
    data = json.dumps(results)

    # Render the HTML template with the chart data
    return render_template('chart.html', data=data)

if __name__ == '__main__':
    app.run()
