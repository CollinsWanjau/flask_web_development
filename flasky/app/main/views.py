from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from flask import flash, Blueprint
from flask_login import login_required, current_user

# main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
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
            with main.app.app_context():
                if main.app.config['IMAGINE_ADMIN']:
                    send_email(main.app.config['IMAGINE_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        # name = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=current_user.username,
                           known = session.get('known', False),
                           current_time=datetime.utcnow())

@main.route('/login')
def login():
    return 'login'

@main.route('/user/<username>')
def profile(username):
    return render_template('user.html', username=username)
    # return '{}\'s profile'.format(escape(username))

"""
with app.test_request_context():
    print(url_for('index', _external=True))
    print(url_for('login', _external=True))
    print(url_for('login', next='/', _external=True))
    print(url_for('profile', username='John Doe', _external=True))
    print(url_for('static', filename='templates'))
"""

@main.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed!'

@main.route('/protected')
@login_required
def protected_page():
    return render_template('index_3.html')

@main.route("/static/favicon.ico")
def fav():
    print(os.path.join(app.root_path, 'templates/static'))
    return send_from_directory(app.static_folder, 'favicon.ico')
