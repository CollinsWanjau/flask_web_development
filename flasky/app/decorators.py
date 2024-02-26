from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission
"""
In a case which an entire view function needs to be made available only to
users with certain permissions, a custom decorator can be used.
The module shows the implementation of two decorators, one for generic
permissions check and one that checks specifically for administrator
permission
"""


def permission_required(permission):
    """These decoratoes are used to restrict access to certain views based
        on the user's role"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)  # Forbidden page
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    """This a decorator created by the permission required decorator.
    It checks if the current_user is an admin or not.
    It takes in a function f as the next action to occur after the
    check happens."""
    return permission_required(Permission.ADMINISTER)(f)
