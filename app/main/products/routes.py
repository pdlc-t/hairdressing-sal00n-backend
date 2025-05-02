from flask import request, jsonify, abort

from app.auth import require_auth
from app.main.products import bp
from app.extensions import db
from app.main.models.product import Product

@bp.route('/', methods=['GET'])
@require_auth
def product_list():
    products = Product.query.all()
    product_list = []
    for prod in products:
        product_list.append({
            "id": prod.id,
            "productName": prod.productName,
            "price": prod.price,
            "amount": prod.amount,
            "producer": prod.producer,
            "description": prod.description
        })
    return jsonify(product_list), 200

@bp.route('/<int:id>', methods=['GET'])
@require_auth
def get_product(id):
    prod = Product.query.get_or_404(id)
    return jsonify({
        "id": prod.id,
        "productName": prod.productName,
        "price": prod.price,
        "amount": prod.amount,
        "producer": prod.producer,
        "description": prod.description
    }), 200

@bp.route('/', methods=['POST'])
@require_auth
def create_product():
    data = request.get_json() or {}
    required = ['productName', 'price', 'amount', 'producer', 'description']
    if not all(field in data for field in required):
        abort(400, 'Missing fields')
    prod = Product(
        productName=data['productName'],
        price=data['price'],
        amount=data['amount'],
        producer=data['producer'],
        description=data['description']
    )
    db.session.add(prod)
    db.session.commit()
    return jsonify({
        "id": prod.id,
        "productName": prod.productName,
        "price": prod.price,
        "amount": prod.amount,
        "producer": prod.producer,
        "description": prod.description
    }), 201

@bp.route('/<int:id>', methods=['PUT'])
@require_auth
def update_product(id):
    prod = Product.query.get_or_404(id)
    data = request.get_json() or {}
    for field in ['productName', 'price', 'amount', 'producer', 'description']:
        if field in data:
            setattr(prod, field, data[field])
    db.session.commit()
    return jsonify({
        "id": prod.id,
        "productName": prod.productName,
        "price": prod.price,
        "amount": prod.amount,
        "producer": prod.producer,
        "description": prod.description
    }), 200

@bp.route('/<int:id>', methods=['DELETE'])
@require_auth
def delete_product(id):
    prod = Product.query.get_or_404(id)
    db.session.delete(prod)
    db.session.commit()
    return jsonify({"message": "Deleted", "id": id}), 200
