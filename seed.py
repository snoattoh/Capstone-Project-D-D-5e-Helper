from app import app
from models import db, User, Board, Piece


db.drop_all()
db.create_all()

db.session.commit()