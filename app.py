from flask import Flask, render_template, request, jsonify
from decimal import Decimal

app = Flask(__name__)

@app.route('/')
def chart_config():
    return render_template('chart.html')

@app.route('/process_tuples', methods=['POST'])
def process_tuples():
    tuples = []
    letters = request.form.getlist('letters[]')
    amounts = request.form.getlist('amounts[]')

    for letter, amount in zip(letters, amounts):
        tuples.append({'letter': letter, 'amount': amount})

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
