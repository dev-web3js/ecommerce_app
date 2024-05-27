import unittest
from app import app, db, bcrypt, create_access_token
from models import User, Product, Order
from cryptography import crypto

class TestEcommerceApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_register(self):
        response = self.app.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 201)
        user = User.query.filter_by(username='testuser').first()
        self.assertTrue(bcrypt.check_password_hash(user.password_hash, 'testpassword'))
        self.assertEqual(crypto.decrypt_data(user.email), 'test@example.com')

    def test_login(self):
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        })
        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_create_order(self):
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com'
        })
        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        access_token = response.get_json()['access_token']
        response = self.app.post('/order', json={
            'product_id': 1,
            'quantity': 2
        }, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
