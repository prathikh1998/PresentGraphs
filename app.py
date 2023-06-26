from flask import Flask, render_template, request, jsonify
import pyodbc
import json
from decimal import Decimal

app = Flask(__name__)

# Azure SQL Database connection settings
server = 'prathikhegde.database.windows.net'
database = 'ASSS2'
username = 'prathikhegde'
password = 'Tco7890$'
driver = '{ODBC Driver 17 for SQL Server}'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Route for displaying the chart configuration form
from flask import Flask, render_template, request, jsonify
from decimal import Decimal

app = Flask(__name__)

@app.route('/')
def chart_config():
    return render_template('chart.html')


@app.route('/process_tuples', methods=['POST'])
def process_tuples():
    tuples = request.form.get('json_data')
    tuples = json.loads(tuples)

    # Perform further processing with the tuples

    # Prepare the data to be sent to index.html
    data = [
        {
            'attribute_value': tuple['letter'],
            'count': Decimal(tuple['amount'])
        }
        for tuple in tuples
    ]

    # Render the index.html template with the data
    return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()
