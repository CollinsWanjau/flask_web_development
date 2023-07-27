from werkzeug.security import generate_password_hash, check_password_hash

from app import db
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

    # Password hashing in User model
    password_hash = db.Column(db.String(128))

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


