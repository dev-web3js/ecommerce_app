from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

from models import User, Product, Order
from controllers import register, login, list_products, create_order

app.route('/register', methods=['POST'])(register)
app.route('/login', methods=['POST'])(login)
app.route('/products', methods=['GET'])(list_products)
app.route('/order', methods=['POST'])(jwt_required()(create_order))

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'))  # Use HTTPS
