# SocialScribe

The purpose of a social media blog app is to provide a platform for bloggers to connect share, and inspire each other through a dynamic social media platform. The app allows users to create and share blog posts, follow other users, and engage with content through comments.The app's features and user experiance should be designed to promote community building and engagement, and to provide a space where bloggers can connect with other like-minded individuals and build a following around their interests. The app also prioritizes security and user privacy, and provide tools for managing user accounts and content.Overall, the purpose of a social media blog app is to provide a platform for bloggers to create and share content, build a community around their interests, and connect with other like-minded individuals.


# Flask

## Variable Rules!
* The `{{ name }}` construct used in the template refs, a variable, a
special placeholder that tells the template engine that the value
that goes in that place should be obtained from data provided at the time
the template is rendered.

* Jinja2 recognizes variables of any type, even complex ones such as lists, tuples, dicts.

```
<p>A value from a dictionary: {{ mydict['key'] }}.<p>
<p>A value from a list: {{ mylist[3] }}.<p>
<p>A value from a list, with a variable index: {{ mylist[myintvar ]}}.</p>
<p>A value from an object's method: {{ myobj.somemthod() }}.<p>
```

* Variables can be modified with filters
`Hello, {{ name|capitalize }}`

* You can add variables sections to a URL by making sections with <variable_name>

* Your function then receives the <variable_name> as a keyword argument.

* Optionally, you can use a converter to specify the type of the arg, like
<converter:variable_name>

## Url Building

* To build a URL to a specific function, use the `url_for()` function.
It accepts the name of the function as its first argument and any number
of keyword arguments, each corresponding to a variable part of the URL
rule.

* Why would you want to build URLs using the URL reversing function
`url_for()` instead of hard-coding them into your templates

1. Reversing is often more descriptive than hard-coding the URLs.
2. You can change your URLs in one one go instead of needing to remember
to manually change hard-coded URLs.
3. URL building handles escaping of special characters and Unicode dta
transparently.
4. The generated paths are always absolute, avoiding unexpected behaviour
of relative paths in browsers.

## Static Files

* To generate URLs for static files, use the special `static` endpoint
name:
```
url_for('static', filename='style.css')
```

* This file has to be stored on the filesystem as `static/style.css`.

# The Request-Response Cycle

## Application and Requests Contexts

* When Flask receives a request from a client, it needs to make a few objects available to the view function that will handle it.

* A good example is the request object, which encapsulates the HTTP request sent by the client.

* To avoid cluttering view functions with lots of args that may or may not be needed, Flask uses contexts to temporarily make certain objects globally accessible.

* Contexts enable Flask to make certain variables globally accessible to a thread without intefering with the other threads.

## Control Structures

```
{% if user %}
    Hello, {{ user }}!
{% else %}
    Hello, Stranger!
{% endif %}
```

* Rendering a list of elements.This example shows how this can be done with
with a for loop.

```
<ul>
    {% for comment in comments %}
        <li>{{ comment }}</li>
    {% endfor %}
</ul>
```

* There is a way to reuse thru `template inheritance`.

## Open a Shell

* To explore data in your app, you can start an interactive Python shell with the
shell command.An app context will be active, and the app instance will be imported.

```
(venv) colloso@colloso-ThinkCentre-M73:~/Documents/flask_web_development/flask_web_development$ flask shell
/index
/login
/login?next=/
/user/John%20Doe
Python 3.10.7 (main, May 29 2023, 13:51:48) [GCC 12.2.0] on linux
App: hello
Instance: /home/colloso/Documents/flask_web_development/flask_web_development/instance
>>> from flask import Flask, url_for
>>> app.config['SERVER_NAME'] = 'localhost:5000'
>>> app.config['APPLICATION_ROOT'] = '/'
>>> app.config['PREFERRED_URL_SCHEME'] = 'http'
>>> with app.app_context():
...     print(url_for('index'))
...     print(url_for('login'))
...     print(url_for('login', next='/'))
...     print(url_for('profile', username='John Doe'))
... 
http://localhost:5000/index
http://localhost:5000/login
http://localhost:5000/login?next=/
http://localhost:5000/user/John%20Doe
>>>
```

## Creating tables in FLask-SQLAlchemy

```
>>> with app.app_context():
...     db.drop_all()
...     db.create_all()
...
```

### Inserting Rows

```
>>> with app.app_context():
...     db.drop_all()
...     db.create_all()
... 
>>> from hello_2 import db, app
>>> from hello_2 import Role, User
>>> admin_role = Role(name='Admin')
>>> mod_role = Role(name='Moderator')
>>> user_role = Role(name='User')
>>> user_john = User(username='john', role=admin_role)
>>> user_susan = User(username='susan', role=user_role)
>>> user_david = User(username='david', role=user_role)
>>> print(admin_role.id)
None

>>> with app.app_context():
...     try:
...         db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan, user_david])
...         db.session.commit()
... 
...         # Now you can access the id attribute directly
...         print(admin_role.id)
...         print(mod_role.id)
...         print(user_role.id)
... 
...     except IntegrityError as e:
...         db.session.rollback()
... 
1
2
3

```

## Modifying rows

* The add() method of the db session can also be used to update models

```
>>> with app.app_context():
...     try:
...         admin_role = Role.query.filter_by(name='Admin').first()
...         admin_role.name = 'Administrator'
...         db.session.add(admin_role)
...         db.session.commit()
...     except IntegrityError as e:
...         db.session.rollback()
...
```

## Querying Rows

```
>>> with app.app_context():
...     Role.query.all()
... 
[<Role 'Administrator'>, <Role 'Moderator'>, <Role 'User'>]

>>> with app.app_context():
...     User.query.all()
... 
[<User 'john'>, <User 'susan'>, <User 'david'>]
```

* It is possible to inspect the native SQL query that SQLALchemy generates for a
given query by converting the query object to a string

```
>>> with app.app_context():
...     str(User.query.filter_by(role=user_role))
... 
'SELECT users.id AS users_id, users.username AS users_username, users.role_id 
AS users_role_id \nFROM users \nWHERE ? = users.role_id'
```

* A query object can be configured to issue more specific db searches thru the
use of filters.The follwing example finds all the users that were assigned the 
"User" role:

```
>>> with app.app_context():
...     users_with_user_role = User.query.join(Role).filter(Role.name == 'User').all()
...     for user in users_with_user_role:
...         print(user.username)
... 
susan
david

```

* Relationships work similarly to queries. The following example queries the
one-to-many relationship between roles and users from both ends:

```
>>> with app.app_context():
...     user_role = Role.query.filter_by(name='User').first()
...     if user_role:
...         users = user_role.users
...         print(users)
... 
[<User 'susan'>, <User 'david'>]

>>> with app.app_context():
...     user_role = Role.query.filter_by(name='User').first()
...     if user_role:
...         users = user_role.users
...         print(users[0].role)
... 
<Role 'User'>
```

* The user_role.users query here has a small problem.The implicit query that
runs when the user_role.users expression is issued internally calls all() to
return the list of users.

* Because the query object is hidden, it is not possible to refine it with
additional query filters.So the configuration is modified with a lazy = 'dynamic'
argument to request that the query is not executed.

# Email Support with Flask-Mail

## Sending Email from the Python Shell

* Testing the configuration, start a shell session and send a test email.

```
(venv) $ python hello.py shell
>>> from flask.ext.mail import Message
>>> from hello import mail
>>> msg = Message('test subject', sender='you@example.com',
...     recipients=['you@example.com'])
>>> msg.body = 'text body'
>>> msg.html = '<b>HTML</b> body'
>>> with app.app_context():
...
mail.send(msg)
...
```

# Large Application Structure

## Project Structure

|-flasky
    |-app/
        |-templates/
        |-static/
        |-main/
            |-__init__.py
            |-errors.py
            |-forms.py
            |-views.py
        |-__init__.py
        |-email.py
        |-models.py
    |-migrations/
    |-tests/
        |-__init__.py
        |-test.py
    |-venv/
    |-requirements.txt
    |-config.py
    |-manage.py

## Configuration Options

* Applications often need several configuration sets. The best example for this
is the need to use different databases during development, testing, and
production so that they don't intefere with each other.


```
cat config.py

import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    IMAGINESTUDIOS_MAIL_SUBJECT_PREFIX = '[Imagine]'
    IMAGINESTUDIOS_MAIL_SENDER = 'Imagine Admin <tripperskripper@gmail.com>'
    IMAGINE_ADMIN = os.environ.get('IMAGINE_ADMIN')

    """
    Configuration classes define a init_app() class method that takes an
    application instance as an arg
    """
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

```

## Application Package

### Using Application Factory

* Using an application factory we can make changes dynamically, this is
particularly important for unittests because sometimes it is necessary
to run the application under different configuration settings for better
test coverage.

* This not only gives the script time to set the configuration but also the
ability to create multiple app instances.The application factory function is
defined in the app package constructor.

[app](app/__init__.py)

## Implementing Application Functionality in a Blueprint

* FLask offers a solution for routing at runtime using `blueprints`.

* The difference is that routes associated with a blueprint are in a dorminant
state until the blueprint is registered with an application, at which point the
routes become part of it.

* To allow for the greatest flexibility, a subpackage inside the app package
will be created to host the blueprint.

[solution](app/main/__init__.py)

