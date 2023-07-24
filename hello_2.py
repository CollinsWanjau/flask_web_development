from flask import Flask, escape, url_for, render_template, send_from_directory, redirect, session, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os

app = Flask(__name__, static_folder='templates/static')
moment = Moment(app)
"""
The app.config dictionary is a general_purpose place to store configuration variables
used by the framework
"""
app.config['SECRET_KEY'] = 'PicaSo420~!@#'
"""
The render template integrates the Jinja2 template engine with the app.

Keywords args like name=name, the name on the left side represents the
arg name, which is used.

The name on the right is a variable in the current scope that provides
the value for the arg of the same name
"""
class NameForm(Form):
    # The validators is set to required(), meaning this field cannot be empty
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        # name = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    return render_template('user.html', username=username)
    # return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index', _external=True))
    print(url_for('login', _external=True))
    print(url_for('login', next='/', _external=True))
    print(url_for('profile', username='John Doe', _external=True))
    print(url_for('static', filename='templates'))

@app.route("/static/favicon.ico")
def fav():
    print(os.path.join(app.root_path, 'templates/static'))
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

bootstrap = Bootstrap(app)

if __name__ == '__main__':
    app.run(debug=True)
