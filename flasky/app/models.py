from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import db
from . import login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app
from . import db

class Permission:
    FOLLOW = 0x01
    COMMENT = 0X02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

# Role model definition
class Role(db.Model):
    # tablename is used to override the table name
    __tablename__ = 'roles'

    # The types of the column are the first arg to Column
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # an improved version of roles permissions
    """db.column: is a class in SQLA that represents a column in a db table
        db.Boolean: specifies the column should be of type Boolean, meaning
        it can only have two values
        index=True: specifies that an index should be created for this column
        which can improve query perfomance"""
    default = db.Column(db.Boolean, default=False, index=True)

    """This field is an integer that will be used as bit flags.Each task
        will be assigned a bit position, and for each role the tasks that
        are allowed for that role will bits set to 1."""
    permissions = db.Column(db.Integer)

    def __repr__(self):
        return '<Role %r>' % self.name

    # relationships
    """The backref arg to db.relationship defines the reverse direction of
    the relationship by adding a role attribute to the User model.This attr
    can be used instead of role_id to access the Role model as an object
    instead of a foreign key"""
    users = db.relationship('User', backref='role', lazy='dynamic')

    # Create roles in the database
    @staticmethod
    def insert_roles():
        """This function does not directly create new role objects.Instead, it
            tries to find existing roles by name and update those.
            To add a new role or change the permission assignments for a role,
            change the roles array and return the function."""
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

# User model definition
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # Updates to the user model to support user logins
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    # This is a one-to-many relationship as ForeignKey is used
    role_id = db.column(db.Integer, db.ForeignKey('roles.id'))


    def __repr__(self):
        return '<User %r>' % self.username
    # relationships
    # the role_id column added is defined as a FK, and that establishes the
    # relationship
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    # Password hashing in User model
    password_hash = db.Column(db.String(128))

    # Define a default role for users
    def __init__(self, **kwargs):
        """kwargs allows the __init__() method to accept an arbitrary number
            of kwargs, which can be used to set the attribute of the user
            object.This is useful wh as it allows any additional kwargs
            to be passed to the parent constructor."""
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['IMAGINE_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    """This decorator is used above the method def to create a read-only
    property"""
    @property
    def password(self):
        """
        Defines a method called password that takes self as an argument.
        The self refers to the instance of the class, allowing access
        to the object's attrs
        Attr Error is raised when attempting to read the passowrd
        """
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        Args:
            self: instance of the class
            password: plain-text password that needs to be hashed and stored
            securely
        Acts as setter for the property.The generate function will hash the
        password and return a secure representation of it.The resulting hash
        is then stored in the password_hash
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Used to verify whether a given plaintext password matches the
        hashed password stored in the password_hash attr
        The function below returns true if the hashed passwords match
        """
        return check_password_hash(self.password_hash, password)

    # User account confirmation
    confirmed = db.Column(db.Boolean, default=False)

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], salt="activate")
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'], salt="activate")
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    # password reset
    def generate_reset_token(self):
        """Generates a password reset token by serializing a dictionary with
        the user's ID and then converts the serialized token to a UTF.This token
        can be used to verify the user's identity when they try to reset their
        password.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id})


    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password = new_password
        db.session.add(user)
        return True

    def generate_email_change_token(self, new_email):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps(
                {'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    # Evaluate whether a user has a given permission
    def can(self, permissions):
        """A helper method to the user model that checks whether a given
            permission is present."""
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)


# Evaluate whether a user has a given permission
class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

# User loader callback function
@login_manager.user_loader
def load_user(user_id):
    """
    Flask requires the app to set up a callback function that loads a user,
    given the identifier.
    The function receives a user identifier as a Unicode string.The return
    value of the function must be the user object if available or None.
    """
    return User.query.get(int(user_id))
