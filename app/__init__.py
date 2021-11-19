from flask import Flask
from app import routes

def create_app():
    app = Flask(__name__)

    app.config['JSON_SORT_KEYS'] = False

    routes.init_app(app)

    return app