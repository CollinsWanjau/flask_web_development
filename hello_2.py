from flask import Flask, escape, url_for, render_template, send_from_directory, redirect, session, flash
from markupsafe import escape
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder='templates/static')



"""
The db connection URI used for the default engine.It can be either a string
or a SQLAlchemy URL instance.
"""
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# Initialize FLask extensions
# db.init_app(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db, directory='migrations')


# Create the Manager instance
# manager = Manager(app)

# Add the MigrateCommand to the manager
# manager.add_command('db', MigrateCommand)

# Flask-Mail configuration for Gmail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['IMAGINESTUDIOS_MAIL_SUBJECT_PREFIX'] = '[Imagine]'
app.config['IMAGINESTUDIOS_MAIL_SENDER'] = 'Imagine Admin <tripperskripper@gmail.com>'
app.config['IMAGINE_ADMIN'] = os.environ.get('IMAGINE_ADMIN')

# Create a Flask-Mail object
mail = Mail(app)

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

# Role model definition
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

    # relationships
    """The backref arg to db.relationship defines the reverse direction of
    the relationship by adding a role attribute to the User model.This attr
    can be used instead of role_id to access the Role model as an object
    instead of a foreign key"""
    users = db.relationship('User', backref='role', lazy='dynamic')

# User model definition
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username
    # relationships
    # the role_id column added is defined as a FK, and that establishes the
    # relationship
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

# Function to set up the shell context
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'User': User, 'Role': Role}

# Email support
def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['IMAGINESTUDIOS_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['IMAGINESTUDIOS_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

@app.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    form = NameForm()
    if form.validate_on_submit():
        # old_name = session.get('name')
        user = User.query.filter_by(username=form.name.data).first()
        #if old_name is not None and old_name != form.name.data:
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['IMAGINE_ADMIN']:
                send_email(app.config['IMAGINE_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        # name = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), known = session.get('known', False), current_time=datetime.utcnow())

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
