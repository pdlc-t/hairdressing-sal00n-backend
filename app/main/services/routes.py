from flask import request, jsonify, abort
from app.main.services import bp
from app.extensions import db
from app.main.models.service import Service

@bp.route('/', methods=['GET'])
def service_list():
    services = Service.query.all()
    service_list = []
    for svc in services:
        service_list.append({
            "id": svc.id,
            "serviceName": svc.serviceName,
            "price": svc.price,
            "time": svc.time,
            "availability": svc.availability,
            "description": svc.description
        })
    return jsonify(service_list), 200

@bp.route('/<int:id>', methods=['GET'])
def get_service(id):
    svc = Service.query.get_or_404(id)
    return jsonify({
        "id": svc.id,
        "serviceName": svc.serviceName,
        "price": svc.price,
        "time": svc.time,
        "availability": svc.availability,
        "description": svc.description
    }), 200

@bp.route('/', methods=['POST'])
def create_service():
    data = request.get_json() or {}
    required = ['serviceName', 'price', 'time', 'availability', 'description']
    if not all(field in data for field in required):
        abort(400, 'Missing fields')
    svc = Service(
        serviceName=data['serviceName'],
        price=data['price'],
        time=data['time'],
        availability=data['availability'],
        description=data['description']
    )
    db.session.add(svc)
    db.session.commit()
    return jsonify({
        "id": svc.id,
        "serviceName": svc.serviceName,
        "price": svc.price,
        "time": svc.time,
        "availability": svc.availability,
        "description": svc.description
    }), 201

@bp.route('/<int:id>', methods=['PUT'])
def update_service(id):
    svc = Service.query.get_or_404(id)
    data = request.get_json() or {}
    for field in ['serviceName', 'price', 'time', 'availability', 'description']:
        if field in data:
            setattr(svc, field, data[field])
    db.session.commit()
    return jsonify({
        "id": svc.id,
        "serviceName": svc.serviceName,
        "price": svc.price,
        "time": svc.time,
        "availability": svc.availability,
        "description": svc.description
    }), 200

@bp.route('/<int:id>', methods=['DELETE'])
def delete_service(id):
    svc = Service.query.get_or_404(id)
    db.session.delete(svc)
    db.session.commit()
    return jsonify({"message": "Deleted", "id": id}), 200
