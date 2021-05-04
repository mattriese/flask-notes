"""Forms for notes app."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Length, URL, Optional

class RegisterForm(FlaskForm):
    """Form for register a user """

    username = StringField("Enter Username",
                           validators=[InputRequired()])
    password = PasswordField("Enter a password",
                             validators=[InputRequired()])
    email = StringField("Enter your email",
                        validators=[InputRequired()])
    first_name = StringField("Enter your first name",
                             validators=[InputRequired()])
    last_name = StringField("Enter your last name",
                            validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form to Login User """

    username = StringField("Enter Username",
                           validators=[InputRequired()])
    password = PasswordField("Enter a password",
                             validators=[InputRequired()])

