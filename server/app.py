# server/app.py

from flask import Flask, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, User, Review, Game

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return "Index for Game/Review/User API"

# start building your API here
@app.route('/games')
def games():
    games = [game.to_dict(only=('title','genre','platform','price')) for game in Game.query.all()]
    response = make_response(
        games,
        200
    )
    return response

@app.route('/games/<int:id>')
def game_by_id(id):
    game = Game.query.get(id)
    if game:
        response_body = game.to_dict()
        #response_body = game.to_dict(only=('title','genre','platform','price'))
        status_code = 200
    else:
        response_body = f'Game {id} not found'
        status_code = 404
    response = make_response(
        response_body,
        status_code
    )
    return response

@app.route('/games/users/<int:id>')
def game_users_by_id(id):
    game = Game.query.filter(Game.id == id).first()
    if game:
        response_body = [user.to_dict() for user in game.users]
    else:
        response_body = "not found"

    response = make_response(
        response_body,
        200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)

