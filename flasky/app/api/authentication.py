from flask_httpauth import HTTPBasicAuth
from ..models import User
from .errors import unauthorized, forbidden
from . import api

# Initializing Flask-HTTPAuth Initialization
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email_or_token, password):
    '''
    The email and password are verified using the existing support
    in the User model.The verification callback returns True when
    the login is valid or False otherwise.g is a global object.
    '''
    if email_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email_or_token.lower()).first()
    if not user:
        return False
    g.current_user = user
    g.token_user = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    '''
    When the authentication credentials are invlaid, the servers
    returns a 401 error to the client.Flask-HTTPAuth generates a
    response with this status code by deafult.'''
    return unauthorized('Invalid credentials')

# the before_request is used to prevent unauthenticated users from
# accessing certain endpoints in your API.The decorator is used to
# run a function before each request is processed.
@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration':3600})
