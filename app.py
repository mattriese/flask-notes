"""Flask app for notes."""

from flask import Flask, render_template, redirect, flash, jsonify

from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User
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
    