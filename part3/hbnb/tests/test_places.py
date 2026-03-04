import unittest

from hbnb.app.models.place import Place
from hbnb.app.models.user import User
from hbnb.app.models.review import Review
from hbnb.app.models.amenity import Amenity


class TestPlaceModel(unittest.TestCase):

    def setUp(self):
        """
        Create a user used as owner for places.
        """
        self.owner = User(
            first_name="Alice",
            last_name="Smith",
            email="alice@example.com"
        )

    def test_create_place_valid(self):
        """
        Test valid place creation.
        """
        place = Place(
            title="Cozy Apartment",
            description="Nice place",
            price=120,
            latitude=45.0,
            longitude=5.0,
            owner=self.owner
        )

        self.assertEqual(place.title, "Cozy Apartment")
        self.assertEqual(place.price, 120)
        self.assertEqual(place.owner_id, self.owner.id)

    def test_place_invalid_price(self):
        """
        Price cannot be negative.
        """
        with self.assertRaises(ValueError):
            Place(
                title="Bad Place",
                description="Invalid price",
                price=-10,
                latitude=45.0,
                longitude=5.0,
                owner=self.owner
            )

    def test_place_invalid_latitude(self):
        """
        Latitude must be between -90 and 90.
        """
        with self.assertRaises(ValueError):
            Place(
                title="Bad Latitude",
                description="Invalid",
                price=50,
                latitude=100,
                longitude=5,
                owner=self.owner
            )

    def test_add_review_to_place(self):
        """
        Test adding a review to a place.
        """
        place = Place(
            title="Test Place",
            description="Review test",
            price=100,
            latitude=45,
            longitude=5,
            owner=self.owner
        )

        review = Review(
            text="Great stay!",
            rating=5,
            user=self.owner,
            place=place
        )

        place.add_review(review)

        self.assertEqual(len(place.reviews), 1)
        self.assertEqual(place.reviews[0].text, "Great stay!")

    def test_add_amenity_to_place(self):
        """
        Test adding amenity to place.
        """
        place = Place(
            title="Amenity Test",
            description="Test",
            price=80,
            latitude=45,
            longitude=5,
            owner=self.owner
        )

        amenity = Amenity(
            name="Wi-Fi",
            description="Fast internet"
        )

        place.add_amenities(amenity)

        self.assertEqual(len(place.amenities), 1)
        self.assertEqual(place.amenities[0].name, "Wi-Fi")
