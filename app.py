"""Flask app for notes."""

from flask import Flask, render_template, redirect, flash, jsonify, session

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, AddNoteForm
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

            user = User.authenticate(username, password) # don't need to call this method, just add them to the session

            if user:
                session["username"] = user.username  #just check for key of username in session.
                return redirect(f"/users/{username}") # could put this at the very top, less nested if/else
            else:
                flash("Authentication failed") # won't need this else clause
                return redirect("/register")

        else:
            flash("Username/email Taken") # move this up to 46
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
            return render_template('login.html', form=form) # added this for failed login
    else:
        return render_template('login.html', form=form)



@app.route("/users/<username>")
def show_secret_page(username):
    """Example hidden page for logged-in users only."""

    if "username" not in session or username != session['username']:
        flash("You must be logged in to view!")
        return redirect("/")

    else:     # don't need else
        user = User.query.filter_by(username=username).first()
        notes = Note.query.all()
        return render_template("secret.html", user=user, notes=notes)


@app.route("/logout")
def logout_user():
    """remove current user's id from session and redirect to home"""

    session.pop("username", None)
    return redirect("/")


@app.route("/users/<username>/delete", methods=["POST"]) # need csfrf so use blank form, also in logout()
def delete_user(username):
    """delete user from the database and delete all notes
    Redirect to / """

    if "username" not in session or username != session['username']: #failling first here good
        flash("You must be logged in to delete!")
        return redirect("/")
    else:    #else not needed
        current_user = User.query.get_or_404(username)
        #notes_from_user = Note.query.filter_by(owner=username).delete() # this could replace for loop (126-129)
        notes_from_user = current_user.notes

        for note in notes_from_user:
            db.session.delete(note)

        db.session.delete(current_user)
        db.session.commit() # pop off session

    return redirect('/')


@app.route("/users/<username>/notes/add", methods=["GET", "POST"])
def add_note_page(username):
    """display add new note page and submit note if post request"""

    if "username" not in session or username != session['username']:
        flash("You must be logged in to view!")
        return redirect("/")

    form = AddNoteForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        owner = username
        note = Note(title=title, content=content, owner=owner)

        db.session.add(note)
        db.session.commit()
        flash("Note added successfully!")

        return redirect(f"/users/{username}")

    else:
        return render_template("add_note.html", form=form, username=username)


@app.route("/notes/<note_id>/update", methods=["GET", "POST"])
def edit_note_page(note_id):
    """display edit note page and submit note edit if post request"""

    note = Note.query.get_or_404(note_id)
    username = note.user.username #could use note.owner
    if "username" not in session or username != session['username']:
        flash("You must be logged in to edit!")
        return redirect("/")

    form = AddNoteForm(obj=note)

    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()
        flash("Note edited successfully!")
        print("note.user.username=, ",  note.user.username)
        return redirect(f"/users/{note.user.username}")

    else:
        return render_template("edit_note.html", form=form, note=note)


@app.route("/notes/<note_id>/delete", methods=["POST"])
def delete_note(note_id):
    """delete note from the database Redirect to /users/<username> """

    note = Note.query.get_or_404(note_id)
    username = note.user.username #note.owner

    if "username" not in session or username != session['username']:
        flash("You must be logged in to delete!")
        return redirect("/")
    else:
        db.session.delete(note)
        db.session.commit()

    return redirect(f"/users/{username}")
