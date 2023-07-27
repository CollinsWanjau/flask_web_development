from flask import Flask, abort
"""
The code returns status code 404 if the id dynamic arg given in the
URL does not represent a valid user
"""


app = Flask(__name__)
@app.route('/user/<id>')
def get_user(id):
    user = load_user(id)
    if not user:
        abort(404)
    return '<h1>Hello, %s</h1>' % user.name
