"""
User endpoint tests.
"""

import unittest
from hbnb.app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        """
        Setup tests client.
        """
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user_valid(self):
        response = self.client.post("/api/v1/users/", json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_email(self):
        response = self.client.post("/api/v1/users/", json={
            "first_name": "Bob",
            "last_name": "Brown",
            "email": "invalid"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_users(self):
        self.client.post("/api/v1/users/", json={
            "first_name": "Test",
            "last_name": "User",
            "email": "tests@example.com"
        })

        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, 200)

    def test_get_user_not_found(self):
        response = self.client.get("/api/v1/users/invalid-id")
        self.assertEqual(response.status_code, 404)
