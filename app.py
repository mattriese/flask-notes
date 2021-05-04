"""Flask app for notes."""

from flask import Flask, render_template, redirect, flash, jsonify, session

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
from forms import RegisterForm, LoginForm
# from forms import AddPetForm, EditPetForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route('/')
def redirect_to_register():
    """homepage redirects to register user page """

    return redirect('/register')

@app.route('/register', methods=["GET", "POST"])
def register_user():
    """handle register user on post or render register user form"""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        taken_username = User.query.filter_by(username=username).first()
        taken_email = User.query.filter_by(email=email).first()

        if not taken_username and not taken_email: # check if username is available

            # create user instance
            user = User.register(username, password, email, first_name, last_name)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful!")

            user = User.authenticate(username, password)

            if user:
                session["username"] = user.username
                return redirect(f"/users/{username}")
            else:
                flash("Authentication failed")
                return redirect("/register")

        else:
            flash("Username/email Taken")
            return render_template("register.html", form=form)
    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login_user():
    """Produce login form or handle login"""

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Bad name/password"]
    else:
        return render_template('login.html', form=form)



@app.route("/users/<username>")
def show_secret_page(username):
    """Example hidden page for logged-in users only."""

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:
        user = User.query.filter_by(username=username).first()
        return render_template("secret.html", user=user)


@app.route("/logout")
def logout_user():
    """remove current user's id from session and redirect to home"""

    session.pop("username", None)
    return redirect("/")
