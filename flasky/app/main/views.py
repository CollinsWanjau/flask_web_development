from datetime import datetime
from flask import render_template, session, redirect, url_for, current_app, request,\
    make_response
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, PostForm, CommentForm 
from .. import db
from ..models import User, Permission, Post, Role, Comment
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
        # Paginate the blog list
        page = request.args.get('page', 1, type=int)
        
        # show followed blog posts in home page
        show_followed = False
        if current_user.is_authenticated:
            show_followed = bool(request.cookies.get('show_followed', ''))
        if show_followed:
            query = current_user.followed_posts
        else:
            query = Post.query
        pagination = query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=current_app.config['IMAGINE_POSTS_PER_PAGE'],
        error_out=False)
        posts = pagination.items
        return render_template('index.html', form=form, posts=posts,
            pagination=pagination, show_followed=show_followed)
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
    # Paginate blog post list
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page=page, per_page=current_app.config['IMAGINE_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts, pagination=pagination)
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

# Permanent links to post
@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    # Blog post comments support
    form = CommentForm()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            # the _get_current_object returns the  actual User object
            comment = Comment(body=form.body.data,
                              post=post,
                              author=current_user._get_current_object())
            db.session.add(comment)
            db.session.commit()
            flash('Your comment has been published.')
            return redirect(url_for('.post', id=post.id, page=-1))
            # handles pagination of comments, by first getting the current page
            # number from the url string
        page = request.args.get('page', 1, type=int)
        # if page is -1, it sets the page number to the last page of comments
        if page == -1:
            page = (post.comments.count()- 1) // \
                current_app.config['IMAGINE_COMMENTS_PER_PAGE'] + 1
        pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(page=page, per_page=current_app.config['IMAGINE_COMMENTS_PER_PAGE'],
            error_out=False)
        comments = pagination.items
        return render_template('post.html', posts=[post], comments=comments,
                               pagination=pagination, form=form)
    else:
        return redirect(url_for('auth.login'))


# Edit blog post route
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTER):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash('The post has been updated.')
        return redirect(url_for('main.post', id=post.id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)

# Follow route and view function
@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are now following %s.' % username)
    return redirect(url_for('.user', username=username))

@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash('You are already following this user.')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following %s anymore.' % username)
    return redirect(url_for('.user', username=username))

# Followers route and view function
@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    # pagination of followers
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page=page, per_page=current_app.config['IMAGINE_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
                for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


# Followed-by route
@main.route('/followed_by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('Invalid user.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page=page, per_page=current_app.config['IMAGINE_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp

@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp
