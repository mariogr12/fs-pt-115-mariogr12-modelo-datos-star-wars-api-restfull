from flask import Flask, request, jsonify, Blueprint
from models import db, User, Character, Planet

api = Blueprint("api", __name__)

#He cambiado el nombre de people a characters para que se entienda mejor
@api.route('/characters', methods=["GET"])
def get_characters():
    characters = Character.query.all()
    if not characters:
        return jsonify({"msn": "There are not characters yet"}), 400
    return jsonify([character.serialize() for character in characters])

#He cambiado el nombre de people a characters para que se entienda mejor
@api.route('/characters/<int:character_id>', methods=["GET"])
def get_character(character_id):
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msn": "character not found"}), 404
    return jsonify(character.serialize()), 200


@api.route('/planets', methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    if not planets:
        return jsonify({"msn": "There are not planets yet"}), 400
    return jsonify([planet.serialize() for planet in planets])


@api.route('/planets/<int:planet_id>', methods=["GET"])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msn": "planet not found"}), 404
    return jsonify(planet.serialize()), 200


@api.route('/users', methods=["GET"])
def get_users():
    users = User.query.all()
    if not users:
        return jsonify({"msn": "There are not users yet"}), 400
    return jsonify([user.serialize() for user in users]), 200


@api.route('/users/<int:user_id>', methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "user not found"}), 404
    return jsonify(user.serialize()), 200


@api.route('/users/<int:user_id>/favorites', methods=["GET"])
def get_user_favorites(user_id):
    user = User.query.get(user_id) 
    if not user:
        return jsonify({"msn": "that user doesn't exist"}), 400
    
    favorites = {
        "favorite_planets": [planet.serialize() for planet in user.favorite_planets],
        "favorite_characters": [character.serialize() for character in user.favorite_characters]
    }

    return jsonify(favorites), 200

@api.route('/users/<int:user_id>/add-favorite-planet/<int:planet_id>', methods=["POST"])
def post_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msn": "user not found"}), 404
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msn": "that planet doesn't exist"}), 400
    
    if planet in user.favorite_planets:
        return jsonify({"msn": "planet already in favorites"}), 400

    user.favorite_planets.append(planet)
    db.session.commit()

    return jsonify(user.serialize()), 200

@api.route('/users/<int:user_id>/add-favorite-character/<int:character_id>', methods=["POST"])
def post_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msn": "user not found"}), 404
    
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msn": "that character doesn't exist"}), 400
    
    if character in user.favorite_characters:
        return jsonify({"msn": "character already in favorites"}), 400

    user.favorite_characters.append(character)
    db.session.commit()

    return jsonify(user.serialize()), 200

@api.route('/users/<int:user_id>/delete-favorite-planet/<int:planet_id>', methods=["DELETE"])
def delete_favorite_planet(user_id, planet_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msn": "user not found"}), 404
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msn": "that planet doesn't exist"}), 400
    
    if planet not in user.favorite_planets:
        return jsonify({"msn": "that planet isn't in favorites"}), 400

    user.favorite_planets.remove(planet)
    db.session.commit()

    return jsonify(user.serialize()), 200

@api.route('/users/<int:user_id>/delete-favorite-character/<int:character_id>', methods=["DELETE"])
def delete_favorite_character(user_id, character_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msn": "user not found"}), 404
    
    character = Character.query.get(character_id)
    if not character:
        return jsonify({"msn": "that character doesn't exist"}), 400
    
    if character not in user.favorite_characters:
        return jsonify({"msn": "that character isn't in favorites"}), 400

    user.favorite_characters.remove(character)
    db.session.commit()

    return jsonify(user.serialize()), 200