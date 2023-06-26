from flask import Flask, render_template, request, jsonify
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
# Route for generating the chart based on user input
@app.route('/generate_chart_population', methods=['POST'])
def generate_chart_population():
    attribute = request.form.get('attribute')
    intervals = request.form.getlist('interval')

    conditions = []
    gt_condition = ""

    for interval in intervals:
        if interval == 'gt':
            gt_condition = f"WHEN {attribute} > '{max_val}' THEN '>{max_val}'"
        else:
            min_val, max_val = interval.split('-')
            condition = f"{attribute} >= '{min_val}' AND {attribute} <= '{max_val}'"
            conditions.append(condition)

    query_statement = " ".join([f"WHEN {condition} THEN '{interval}'" for condition, interval in zip(conditions, intervals) if interval != 'gt'])
    case_statement = " ".join([f"WHEN '{interval}' THEN '{interval}'" for interval, interval in zip(intervals,intervals) if interval != 'gt']) 
    sql_query = f"""
        SELECT {attribute}_range, COUNT(*) AS count
        FROM (
            SELECT CASE {query_statement} {gt_condition} ELSE 'Other' END AS {attribute}_range
            FROM [city-1]
        ) AS subquery
        GROUP BY {attribute}_range
        ORDER BY CASE {attribute}_range {case_statement} {gt_condition} ELSE 'Other' END
    """

    print("Generated SQL query:")
    print(sql_query)



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

#city function

@app.route('/generate_chart_city', methods=['POST'])
def generate_chart_city():
    attribute = request.form.get('attribute')
    intervals = request.form.getlist('interval')

    conditions = []

    for interval in intervals:
        condition = f"{attribute} = '{interval}'"
        conditions.append(condition)

    query_statement = " OR ".join(conditions)

    sql_query = f"""
        SELECT {attribute}, COUNT(*) AS count
        FROM [city-1]
        WHERE {query_statement}
        GROUP BY {attribute}
        ORDER BY {attribute}
    """

    print("Generated SQL query:")
    print(sql_query)

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


# Function to get the number of cities under a given latitude and longitude
@app.route('/get_num_cities', methods=['POST'])
def get_num_cities():
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    conditions = []

    sql_query= f"""
    SELECT City,COUNT(*) FROM [city-1] WHERE lat = {latitude} AND lon = {longitude}"""

    print("Generated SQL query:")
    print(sql_query)

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