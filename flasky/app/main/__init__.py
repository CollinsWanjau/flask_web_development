from flask import Blueprint


main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission

"""Permissions may also need to be checked from templates, so the
Permission class with all the bit constants needs to be accessble to them.
Context processors make variables globally available to all templates.
"""
@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
