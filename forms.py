"""Forms for notes app."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, EmailField
from wtforms.validators import InputRequired, Length, URL, Optional

class RegisterForm(FlaskForm):
    """Form for register a user """

    username = StringField("Enter Username",
                           validators=[InputRequired()])
    password = PasswordField("Enter a password",
                             validators=[InputRequired()])
    email =  EmailField("Enter your email",
                        validators=[InputRequired()])
    first_name = StringField("Enter your first name",
                             validators=[InputRequired()])
    last_name = StringField("Enter your last name",
                            validators=[InputRequired()])                              
