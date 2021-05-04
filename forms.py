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
    email = EmailField("Enter your email",
                        validators=[InputRequired()])
    first_name = StringField("Enter your first name",
                             validators=[InputRequired()])
    last_name = StringField("Enter your last name",
                            validators=[InputRequired()])

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(username=username,
                    password=hashed,
                    email=email,
                    first_name=first_name,
                    last_name=last_name)
