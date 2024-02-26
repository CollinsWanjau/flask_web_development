from flask import Flask, redirect
"""
A redirect is typically indicated with a 302 response status code and
the URL to redirect to given in a Location header.

A redirect response can be generated using a three-value return, or also
with a Response object, but given it's frequent use, Flask provides a
redirect() helper function
"""
app = Flask(__name__)

@app.route('/')
def index():
    return redirect('http://www.example.com')
