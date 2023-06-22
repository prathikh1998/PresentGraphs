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
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Route for displaying the chart in HTML
@app.route('/')
def display_chart():
    # Connect to the database
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Execute the SQL query
    cursor.execute("SELECT magnitude_range, SUM(quake_count) FROM (SELECT CASE WHEN mag < 1 THEN '1. Magnitude < 1' WHEN mag >= 1 AND mag < 2 THEN '2. Magnitude 1-2' WHEN mag >= 2 AND mag < 3 THEN '3. Magnitude 2-3' WHEN mag >= 3 AND mag < 4 THEN '4. Magnitude 3-4' WHEN mag >= 4 AND mag <= 5 THEN '5. Magnitude 4-5' ELSE '6. Magnitude > 5' END AS magnitude_range, COUNT(*) AS quake_count FROM all_month GROUP BY CASE WHEN mag < 1 THEN '1. Magnitude < 1' WHEN mag >= 1 AND mag < 2 THEN '2. Magnitude 1-2' WHEN mag >= 2 AND mag < 3 THEN '3. Magnitude 2-3' WHEN mag >= 3 AND mag < 4 THEN '4. Magnitude 3-4' WHEN mag >= 4 AND mag <= 5 THEN '5. Magnitude 4-5' ELSE '6. Magnitude > 5' END) AS subquery GROUP BY magnitude_range ORDER BY CAST(SUBSTRING(magnitude_range, 1, 1) AS INTEGER)")
    
    # Fetch all the rows
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    results = []
    for row in rows:
        result = {'magnitude_range': row[0], 'quake_count': row[1]}
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
