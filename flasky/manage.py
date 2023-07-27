#!/usr/bin/env python3
import os
import unittest
from app import create_app, db
from app.models import User, Role
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
cli = FlaskGroup(create_app=create_app)

# Initialize Flask-Migrate
migrate = Migrate(app, db, directory='migrations', command='migrate')

# Function to set up the shell context
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User, 'Role': Role}

# Add Flask-Migrate commands to the cli
# cli.add_command('migrate-db', MigrateCommand)

# Command to run unit tests
@app.cli.command()
def test():
    """Run the unit tests"""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    cli()
