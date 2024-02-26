from flask import Flask, escape, , render_template, send_from_directory, flash
from markupsafe import escape




app = Flask(__name__, static_folder='templates/static')



# Create the Manager instance
# manager = Manager(app)

# Add the MigrateCommand to the manager
# manager.add_command('db', MigrateCommand)

# Flask-Mail configuration for Gmail



"""
The render template integrates the Jinja2 template engine with the app.

Keywords args like name=name, the name on the left side represents the
arg name, which is used.

The name on the right is a variable in the current scope that provides
the value for the arg of the same name
"""
if __name__ == '__main__':
    app.run(debug=True)
