from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/get-results")
def get_results():
    query = request.args.get("query")
    # Process the query and retrieve the results (dummy example)
    results = {
        "labels": ["Label 1", "Label 2", "Label 3"],
        "data": [10, 20, 30]
    }
    return jsonify(results)

if __name__ == "__main__":
    app.run()
