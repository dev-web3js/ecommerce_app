from flask import request, jsonify
from app import db, bcrypt, create_access_token, get_jwt_identity
from models import User, Product, Order
from cryptography import crypto

def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    encrypted_email = crypto.encrypt_data(data['email'])
    new_user = User(username=data['username'], password_hash=hashed_password, email=encrypted_email, role='customer')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token)
    return jsonify({"message": "Invalid credentials!"}), 401

def list_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'description': p.description, 'price': p.price, 'stock': p.stock} for p in products])

def create_order():
    data = request.get_json()
    current_user = get_jwt_identity()
    new_order = Order(user_id=User.query.filter_by(username=current_user['username']).first().id,
                      product_id=data['product_id'], quantity=data['quantity'], status='pending')
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created successfully!"}), 201
