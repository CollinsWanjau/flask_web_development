from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm 
from .. import db
from ..models import User, Permission, Post, Role
from flask import flash, Blueprint, send_from_directory
from flask_login import login_required, current_user
import os
from ..email import send_email
from ..decorators import admin_required, permission_required

# main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    # name = None
    # form = NameForm()
    form = PostForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            # the database needs a real user object, which is obtained by _get_current
            post = Post(body=form.body.data,
                        author=current_user._get_current_object())
            db.session.add(post)
            db.session.commit()
            return redirect(url_for('.index'))
        # form.body.data = 'This is my post.'
        posts = Post.query.order_by(Post.timestamp.desc()).all()
        return render_template('index.html', form=form, posts=posts)
    else:
        return redirect(url_for('auth.login'))
"""
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
                           form=form, 
                           name=current_user.username if current_user.is_authenticated else None,
                           known = session.get('known', False),
                           post_form=post_form, posts=posts,
                           current_time=datetime.utcnow())
"""
@main.route('/login')
def login():
    return 'login'

"""
@main.route('/user/<username>')
def profile(username):
    return render_template('user.html', user=user)
    # return '{}\'s profile'.format(escape(username))
"""
@main.route('/user/<username>')
def user(username):
    """the username given in the url is searched in the db"""
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    # posts = user.posts.order_by(Post.timestamp.desc()).all()
    posts = Post.query.filter_by(author=user).order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)
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
    print(os.path.join(current_app.root_path, 'templates/static'))
    return send_from_directory(current_app.static_folder, 'favicon.ico')

"""
@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return "For administrators!"

@main.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return "For comment moderators!"
"""

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    The view function sets initial values for all the fields before presenting
    the form.For any given field, this is done by assigning the initial value to
    form.<field-name>.data.
    """
    form = EditProfileForm()
    if form.validate():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        # get_object is used to map a Python object to a db table
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

# Profile edit route for admins
@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('The profile has been updated.')
        return redirect(usr_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)
