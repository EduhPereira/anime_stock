from flask import Blueprint
from app.controllers.anime_controller import get_create, filter, update, delete

bp = Blueprint("bp_animes", __name__, url_prefix="/animes")

bp.get("")(get_create)
bp.get("/<int:anime_id>")(filter)
bp.post("")(get_create)
bp.patch("/<int:anime_id>")(update)
bp.delete("/<int:anime_id>")(delete)