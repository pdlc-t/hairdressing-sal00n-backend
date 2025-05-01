from flask import request, jsonify, abort
from app.main.products import bp
from app.extensions import db
from app.main.models.product import Product

@bp.route('/', methods=['GET'])
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
def delete_product(id):
    prod = Product.query.get_or_404(id)
    db.session.delete(prod)
    db.session.commit()
    return jsonify({"message": "Deleted", "id": id}), 200
