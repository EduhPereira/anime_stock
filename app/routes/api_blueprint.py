from flask import Blueprint
from app.routes.anime_blueprint import bp as bp_animes

bp = Blueprint("bp_api", __name__, url_prefix="/api")

bp.register_blueprint(bp_animes)