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

