import os, requests

from flask import Flask, render_template, request, flash, redirect, session, g, abort, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, UserEditForm, LoginForm
from models import db, connect_db, User, Board, Piece

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
os.environ.get('DATABASE_URL', 'postgres:///dndboard'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

# def check_logged_in():
#     """We check if we're logged in! It's everywhere! I'm making a function... 
#     Ok maybe not?? maybe I'll figure out a way to do it later... """
#     if not g.user:
#         flash("Access unauthorized.", "danger")
#         return redirect("/")


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(form)
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('user/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('user/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You've successfully logged out!", 'primary')
    return redirect("/")

@app.route('/profile')
def profile():
    """Show Profile of User."""

    if g.user:
        return render_template('user/profile.html')
    else:
        #There's no profile for a non user!
        return redirect("/")

@app.route('/profile/edit', methods=["GET", "POST"])
def edit_user():
    """Edit Profile of User (Self)."""

    if g.user:
        form = UserEditForm()
        if form.validate_on_submit():
            try:
                user = User.update(form, g.user.id)
                do_login(user)
                return render_template('user/profile.html', form=form)
            except:

                return redirect("/")
        else:

            form.bio.data = g.user.bio
            form.email.data = g.user.email
            form.first_name.data = g.user.first_name
            form.last_name.data = g.user.last_name
            form.style.data = g.user.style

            return render_template('user/editprofile.html', form=form)
    else:
        #There's no profile for a non user!
        return redirect("/")


################
# External Routes:

#We'll call the lists of the api on the back end
@app.route('/spells')
def list_spells():
    """Returns a page listing all of the spells
    """
    res = requests.get(
        "https://www.dnd5eapi.co/api/spells").json()

    return render_template('catalogue/lists.html', spells=res)

@app.route('/spells/<index>')
def spell_details(index):
    """Returns a detailed page of index spell
    """

    res = requests.get(
    f"https://www.dnd5eapi.co/api/spells/{index}").json()
    
    return render_template('catalogue/details.html', spell=res)

@app.route('/monsters')
def list_monsters():
    """Returns a page listing all of the monsters
    """

    res = requests.get(
        "https://www.dnd5eapi.co/api/monsters").json()
    return render_template('catalogue/lists.html', monsters=res)


@app.route('/monsters/<index>')
def monster_details(index):
    """Returns a detailed page of index monster
    """

    res = requests.get(
    f"https://www.dnd5eapi.co/api/monsters/{index}").json()

    return render_template('catalogue/details.html', monster=res)




#############################################################################
#Homepage and error pages
#

@app.route('/')
def homepage():
    """Show homepage:

    - anon users: Just a hi
    - logged in: Hi for the user
    """

    if g.user:
        #There's no need to send the user, but it'll check on home.html if there is one for alternate text.
        return render_template('home.html', user=g.user)
    else:
        return render_template('home.html')


##############################################################################
# Turn off all caching in Flask
#   (useful for dev; in production, this kind of stuff is typically
#   handled elsewhere)
#
# https://stackoverflow.com/questions/34066804/disabling-caching-in-flask

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req
