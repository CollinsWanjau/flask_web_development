from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField, TextAreaField, \
        BooleanField, SelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, Regexp
from flask_pagedown.fields import PageDownField

class NameForm(Form):
    # The validators is set to required(), meaning this field cannot be empty
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

# profile edit form
class EditProfileForm(Form):
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

# Profile editing form for administrators
class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    confirmed = BooleanField('Confirmed')

    """Implements a dropwdown list, used in this form to select a user role
    An instnce of SelectField must have the items set in its choices attr."""
    role = SelectField('Role', coerce=int)
    name = StringField('Real name', validators=[Length(0, 64)])
    location = StringField('Location', validators=[Length(0, 64)])
    about_me = TextAreaField('About me')
    submit = SubmitField('Submit')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=filed.data).first():
            raise ValidationError('Username already in user.')

# Blog post form
class PostForm(Form):
    body = PageDownField("What's on your mind?", validators=[DataRequired()])
    submit = SubmitField('Submit')

# Comment input form
class CommentForm(Form):
    body = StringField('Enter your comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
