# importing flask class
from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    user_agent = request.headers.get('User-Agent')
    return '<p>Your browser is %s</p>' % user_agent
    # return '<h1>Hello World!<h1>'

@app.route("/")
def hello_world():
    return "Hello, world!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
