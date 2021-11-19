import psycopg2
from app.models.anime_model import AnimeModel
from flask import jsonify, request
from app.exceptions import InvalidKeys

def get_create():
    if request.method == "GET":
        return jsonify(AnimeModel.read_all()), 200
    
    if request.method == "POST":
        data = request.get_json()
        try:
            AnimeModel.validate(data.keys())
            anime = AnimeModel(**data)
            return jsonify(anime.create()), 201
        except (psycopg2.Error, InvalidKeys) as e:
            if type(e).__name__ == 'InvalidKeys':
                return jsonify(e.message), 422
            else:
                return {"error":"anime already exists"}, 409

def filter(anime_id):
    try:
        return jsonify(AnimeModel.read_by_id(anime_id)), 200
    except TypeError:
        return {}, 404

def update(anime_id):
    data = request.get_json()
    try:
        AnimeModel.validate(data.keys())
        update_anime = AnimeModel.update(anime_id, data)
        return jsonify(update_anime), 200
    except (TypeError, InvalidKeys) as e:
        if type(e).__name__ == 'InvalidKeys':
            return jsonify(e.message), 422
        else:
            return {}, 404

def delete(anime_id):
    try:
        AnimeModel.delete(anime_id)
        return {}, 204
    except TypeError:
        return {}, 404
