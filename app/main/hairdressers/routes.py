from flask import request, jsonify, abort
from app.main.hairdressers import bp
from app.extensions import db
from app.main.models.hairdresser import Hairdresser
import json

@bp.route('/', methods=['GET'])
def hairdresser_list():
    hairdressers = Hairdresser.query.all()
    result = []
    for hd in hairdressers:
        result.append({
            "id": hd.id,
            "firstName": hd.firstName,
            "lastName": hd.lastName,
            # zapisujemy listę specjalności jako Python listę
            "specialties": json.loads(hd.specialties),
            "rating": hd.rating
        })
    return jsonify(result), 200

@bp.route('/<int:id>', methods=['GET'])
def get_hairdresser(id):
    hd = Hairdresser.query.get_or_404(id)
    return jsonify({
        "id": hd.id,
        "firstName": hd.firstName,
        "lastName": hd.lastName,
        "specialties": json.loads(hd.specialties),
        "rating": hd.rating
    }), 200

@bp.route('/', methods=['POST'])
def create_hairdresser():
    data = request.get_json() or {}
    required = ['firstName', 'lastName', 'specialties', 'rating']
    if not all(field in data for field in required):
        abort(400, description="Missing fields")
    hd = Hairdresser(
        firstName = data['firstName'],
        lastName  = data['lastName'],
        specialties = json.dumps(data['specialties']),
        rating = data['rating']
    )
    db.session.add(hd)
    db.session.commit()
    return jsonify({
        "id": hd.id,
        "firstName": hd.firstName,
        "lastName": hd.lastName,
        "specialties": data['specialties'],
        "rating": hd.rating
    }), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_hairdresser(id):
    hd = Hairdresser.query.get_or_404(id)
    data = request.get_json() or {}
    if 'firstName' in data:
        hd.firstName = data['firstName']
    if 'lastName' in data:
        hd.lastName = data['lastName']
    if 'specialties' in data:
        hd.specialties = json.dumps(data['specialties'])
    if 'rating' in data:
        hd.rating = data['rating']
    db.session.commit()
    return jsonify({
        "id": hd.id,
        "firstName": hd.firstName,
        "lastName": hd.lastName,
        "specialties": json.loads(hd.specialties),
        "rating": hd.rating
    }), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_hairdresser(id):
    hd = Hairdresser.query.get_or_404(id)
    db.session.delete(hd)
    db.session.commit()
    return jsonify({
        "message": "Deleted",
        "id": id
    }), 200
