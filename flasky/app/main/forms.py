from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class NameForm(Form):
    # The validators is set to required(), meaning this field cannot be empty
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')
