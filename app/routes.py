from flask import Blueprint, jsonify, request, abort, make_response
from app.models import User
from app import db,create_app
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        abort(400, description="Missing email or password")

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        abort(401, description="Invalid credentials")

    access_token = create_access_token(identity=str(user.id))
    
    return jsonify({
        'access_token': access_token,
        'message': 'Login successful',
        'user_id': user.id
    }), 200

@bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({'message': 'Logout successful'}))
    response.delete_cookie('access_token')
    return response

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        abort(400, description="Missing email or password")

    # Optional: Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        abort(409, description="Email already registered")

    user = User(email=data['email'],password_hash=data['password'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully', 'user_id': user.id}), 201

@bp.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        abort(404, description="User not found")

    return jsonify(user.to_dict()), 200

