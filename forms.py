"""Forms for notes app."""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Length, URL, Optional

class RegisterForm(FlaskForm):
    """Form for register a user """

    username = StringField("Enter Username",
                           validators=[InputRequired()])
    password = PasswordField("Enter a password",
                             validators=[InputRequired()]) # add length validator
    email = StringField("Enter your email",
                        validators=[InputRequired()]) # add email validator and EmailField
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


class AddNoteForm(FlaskForm):
    """Form to add a new note"""

    title = StringField("Title:",
                        validators=[InputRequired()])
    content = TextAreaField("Note:",
                            validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """deleteform intetnionally left blank """
