from flask import Flask, Blueprint, request, render_template
from flask_mongoengine import MongoEngine
from server.routes import create_routes
from flask_cors import CORS, cross_origin
from server import utils
from server import models

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(create_routes(Blueprint, request, utils, models))

    app.config['MONGODB_SETTINGS'] = {
        'db': 'calendario',
        'host': 'localhost:27017'
    }

    db = MongoEngine()
    db.init_app(app)

    return app
