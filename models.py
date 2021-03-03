"""Models for Capstone app."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://thumbs.dreamstime.com/b/default-avatar-profile-vector-user-profile-default-avatar-profile-vector-user-profile-profile-179376714.jpg"

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    # usernameid = db.Column(
    #     db.Text,
    #     nullable=False,
    #     unique=True,
    # )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    # discriminator = db.Column(
    #     db.Integer,
    #     nullable=False
    # )

    role = db.Column(
        db.Text
    )

    bio = db.Column(
        db.Text
    )

    first_name = db.Column(
        db.Text
    )

    last_name = db.Column(
        db.Text
    )

    style = db.Column(
        db.Text
    )

    join_date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),

    )

    avatar = db.Column(
        db.Text,
        default=DEFAULT_IMAGE_URL,
    )

    def __repr__(self):
        return f"<User #{self.usernameid}: {self.username}, {self.email}, {self.first_name}"
    
    @classmethod
    def signup(cls, form):
        """Sign Up

        Hash Password
        """
        hashwrd = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        # usernameid = checkdiscriminator(form.username.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashwrd,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
        )

        db.session.add(user)
        return user
    
    @classmethod
    def update(cls, form, userid):
        """Update User
        """
        user = cls.query.filter_by(id=userid).first()

        if user:
            is_auth = cls.authenticate(user.username, form.data.password)
            if is_auth:
                user.data['email'] = form.email.data
                user.data['first_name'] = form.first_name.data
                user.data['last_name'] = form.last_name.data
                user.data['style'] = form.style.data
                user.data['bio'] = form.bio.data
                db.session.commit()
                
            return user
        return False

    
    @classmethod
    def authenticate(cls, username, password):
        """
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    # @classmethod
    # def checkdiscriminator(cls, username):
    #     """Generates a discriminator for the username
    #     """



class Board(db.Model):
    """Boards of D&D pieces."""

    __tablename__ = 'boards'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.Text,
        nullable=False
    )

    link = db.Column(
        db.Text,
        nullable=False
    )
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

    user = db.relationship('User')

class Piece(db.Model):
    """Item Pieces."""

    __tablename__ = 'pieces'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    image = db.Column(
        db.Text,
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    size = db.Column(
        db.Text,
        nullable=False
    )

    board_id = db.Column(
        db.Integer,
        db.ForeignKey('boards.id', ondelete='CASCADE'),
        nullable=False,
    )

    board = db.relationship('Board')

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)