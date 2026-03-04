"""
Review endpoint tests.
"""

import unittest
from hbnb.app import create_app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Create user
        user_response = self.client.post("/api/v1/users/", json={
            "first_name": "Reviewer",
            "last_name": "User",
            "email": "reviewer@example.com"
        })
        self.user_id = user_response.json["id"]

        # Create place
        place_response = self.client.post("/api/v1/places/", json={
            "title": "Nice Place",
            "description": "Test",
            "price": 50,
            "latitude": 45.0,
            "longitude": 10.0,
            "owner_id": self.user_id
        })
        self.place_id = place_response.json["id"]

    def test_create_review_valid(self):
        response = self.client.post("/api/v1/reviews/", json={
            "text": "Great!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_invalid_rating(self):
        response = self.client.post("/api/v1/reviews/", json={
            "text": "Bad rating",
            "rating": 10,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_delete_review(self):
        review = self.client.post("/api/v1/reviews/", json={
            "text": "To delete",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = review.json["id"]

        delete_response = self.client.delete(f"/api/v1/reviews/{review_id}")
        self.assertEqual(delete_response.status_code, 200)
