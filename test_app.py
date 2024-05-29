import unittest
from flask_testing import TestCase
from flask import Flask
from app import app
from models import db, connect_db, User

class FlaskRouteTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:01302@localhost/test_db'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_test_user(self):
        test_user = User(first_name='TestFirstName', last_name='TestLastName', image_URL='TestImgUrl.com')
        db.session.add(test_user)
        db.session.commit()
        return test_user

    def test_users_list_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        users = User.query.all()
        for user in users:
            self.assertIn(user.first_name.encode(), response.data)

    def test_add_user_route_post(self):
        num_users_before = User.query.count()

        response = self.client.post ('/add_user_form', data={
            'first-name': 'TestFirstName',
            'last-name': 'TestLastName',
            'img-url': 'TestImgURL.com'
        })

        num_users_after = User.query.count()

        self.assertEqual(num_users_after, num_users_before +1)
        self.assertEqual(response.status_code, 302)

    def test_add_user_route_get(self):
        response = self.client.get('/add_user_form')
        self.assertEqual(response.status_code, 200)

    def test_show_user_route(self):
        test_user = self.create_test_user()

        response = self.client.get(f'/{test_user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(test_user.first_name.encode(), response.data)

    def test_edit_user_post(self):
        test_user = self.create_test_user()

        response = self.client.post(f'/{test_user.id}/edit_user_form', data={
            'first-name': 'NewFirstName',
            'last-name': 'NewLastName',
            'img-url': 'NewImgUrl.com'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_user.first_name,'NewFirstName')
        self.assertEqual(test_user.last_name, 'NewLastName')
        self.assertEqual(test_user.image_URL, 'NewImgUrl.com')

    def test_delete_user_post(self):
        test_user = self.create_test_user()

        response = self.client.post(f'/{test_user.id}/delete')
        user = User.query.get(test_user.id)
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
