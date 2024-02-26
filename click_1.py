import click
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name

@click.group()
def cli():
    pass

@cli.command()
@click.option('--host', default='127.0.0.1', help='The host address to bind the server to.')
@click.option('--port', default=5000, help='The port number to run the server on.')
@click.option('--debug/--no-debug', default=True, help='Enable or disable debug mode.')
def runserver(host, port, debug):
    """Run the Flask development server."""
    app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    cli()

