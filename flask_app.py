from flask import Flask, request

app = Flask(__name__)


@app.route("/hello", methods=['GET', 'POST'])
def hello():
    name = request.args.get('name')
    if not name:
        req_body = request.get_json()
        if req_body:
            name = req_body['name']

    if name:
        return f"Hello, {name}. This HTTP triggered function executed successfully."
    else:
        return "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response."


@app.route("/foo", methods=['GET'])
def foo():
    return "test"


@app.route("/bar", methods=['POST'])
def bar():
    return request.get_json()


if __name__ == "__main__":
    app.run(debug=True)
