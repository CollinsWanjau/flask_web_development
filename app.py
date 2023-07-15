# importing flask class
from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!<h1>'

@app.route("/")
def hello_world():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
