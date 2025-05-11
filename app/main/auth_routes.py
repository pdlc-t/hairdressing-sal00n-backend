from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.main.models.client import Client
import jwt
import datetime
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    print('Received data from frontend:', data)
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the user already exists
    if Client.query.filter_by(login=data['email']).first():
        return jsonify({'error': 'User already exists'}), 400

    # Create a new user
    hashed_password = generate_password_hash(data['password'])
    new_client = Client(
        first_name="Default",
        second_name="User",
        login=data['email'],
        password_hash=hashed_password
    )
    db.session.add(new_client)
    db.session.commit()

    # Generate JWT token
    token = jwt.encode(
        {
            'user_id': new_client.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({'message': 'User registered successfully', 'token': token}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "password")):
        return jsonify({'error': 'Missing required fields'}), 400

    # Find the user
    client = Client.query.filter_by(login=data['username']).first()
    if not client or not check_password_hash(client.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate JWT token
    token = jwt.encode(
        {
            'user_id': client.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    return jsonify({'message': 'Login successful', 'token': token}), 200