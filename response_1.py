from flask import Flask, make_response
"""
The make_reponse function takes one, two or three args, the same
values that can be returned from a view function, and returns
a Response Object.
"""
app = Flask(__name__)
@app.route('/')
def index():
    response = make_response('<h1>This document carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response
