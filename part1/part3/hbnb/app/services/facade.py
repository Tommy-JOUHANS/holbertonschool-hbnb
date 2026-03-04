"""
Facade layer connecting API and business logic.
"""

from hbnb.app.models import User, Place, Review, Amenity
from hbnb.app.persistence.repository import InMemoryRepository


class HBnBFacade:

    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # =========================
    # USER
    # =========================

    def create_user(self, user_data):
        existing_user = self.user_repo.get_by_attribute("email", user_data["email"])
        if existing_user:
            raise ValueError("Email already exists")
        
        user = User(**user_data)
        
        self.user_repo.add(user)
        
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    # =========================
    # AMENITY
    # =========================

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def add_amenity_to_place(self, place_id, amenity_id):

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        place.add_amenities(amenity)
        return place

    # =========================
    # PLACE
    # =========================

    def create_place(self, place_data):

        owner = self.user_repo.get(place_data["owner_id"])

        if not owner:
            raise ValueError("Owner not found")

        place = Place(**place_data)

        self.place_repo.add(place)

        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    """ Update place with new data """
    def update_place(self, place_id, update_data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        place.update(update_data)
        return place

    # =========================
    # REVIEW
    # =========================

    def create_review(self, review_data):
        """ Validate place and user existence before creating review """
        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])
        
        if not place:
            raise ValueError("Place not found")
        
        if not user:
            raise ValueError("User not found")

        """ Create review and associate with place """
        review = Review(**review_data)

        """ Link review to place and add to place's reviews list """
        
        self.review_repo.add(review)
        
        place.add_review(review)
        
        user.reviews.append(review)
        
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        """ Also remove review from associated place """
        place = review.place

        if place and review in place.reviews:
            place.reviews.remove(review)
        """ Finally, delete review from repository """
        self.review_repo.delete(review_id)
    