"""
Facade layer connecting API and business logic.
Supports both in-memory and database persistence.
"""
import os
from hbnb.app.models import User, Place, Review, Amenity
from hbnb.app.persistence import get_repository

# Determine which repository to use based on environment
USE_DATABASE = os.getenv('USE_DATABASE', 'false').lower() == 'true'

if USE_DATABASE:
    from hbnb.app.persistence.repository import SQLAlchemyRepository as RepositoryClass
    print("Using SQLAlchemy Repository")
else:
    from hbnb.app.persistence.repository import InMemoryRepository as RepositoryClass
    print("Using InMemory Repository")


class HBnBFacade:
    def __init__(self):
        """Initialize repositories based on configuration"""
        if USE_DATABASE:
            self.user_repo = RepositoryClass(User)
            self.place_repo = RepositoryClass(Place)
            self.review_repo = RepositoryClass(Review)
            self.amenity_repo = RepositoryClass(Amenity)
        else:
            self.user_repo = RepositoryClass()
            self.place_repo = RepositoryClass()
            self.review_repo = RepositoryClass()
            self.amenity_repo = RepositoryClass()

    # =========================
    # UTILS
    # =========================

    def save(self):
        """Sauvegarder les changements en base"""
        if USE_DATABASE:
            from hbnb.app import db
            db.session.commit()

    # =========================
    # USER
    # =========================

    def create_user(self, user_data):
        """Create a new user with validation"""
        existing_user = self.get_user_by_email(user_data["email"])
        if existing_user:
            raise ValueError("Email already exists")
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get user by ID"""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get user by email address"""
        return self.user_repo.get_by_attribute("email", email)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, update_data):
        """Update user with new data"""
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        user.update(update_data)
        return user

    # =========================
    # AMENITY
    # =========================

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, update_data):
        """Update amenity with new data"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        amenity.update(update_data)
        return amenity

    def add_amenity_to_place(self, place_id, amenity_id):
        """Add amenity to a place"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if amenity in place.amenities:
            raise ValueError("Amenity already linked to this place")

        place.amenities.append(amenity)  # ✅ direct sur la relation SQLAlchemy

        if USE_DATABASE:
            from hbnb.app import db
            db.session.commit()

        return place

    def remove_amenity_from_place(self, place_id, amenity_id):
        """Remove amenity from a place"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")

        if amenity not in place.amenities:
            raise ValueError("Amenity not linked to this place")

        place.amenities.remove(amenity)

        if USE_DATABASE:
            from hbnb.app import db
            db.session.commit()

        return place

    # =========================
    # PLACE
    # =========================

    def create_place(self, place_data):
        """Create a new place"""
        owner = self.user_repo.get(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, update_data):
        """Update place with new data"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        place.update(update_data)
        return place

    def delete_place(self, place_id):
        """Delete a place by ID"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        if hasattr(place, 'reviews') and place.reviews:
            for review in place.reviews[:]:
                self.review_repo.delete(review.id)

        self.place_repo.delete(place_id)

    # =========================
    # REVIEW
    # =========================

    def create_review(self, review_data):
        """Validate place and user existence before creating review"""
        user = self.user_repo.get(review_data["user_id"])
        place = self.place_repo.get(review_data["place_id"])

        if not place:
            raise ValueError("Place not found")
        if not user:
            raise ValueError("User not found")

        review = Review(**review_data)
        self.review_repo.add(review)

        if hasattr(place, 'add_review'):
            place.add_review(review)

        if USE_DATABASE:
            from hbnb.app import db
            db.session.commit()

        return review

    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews
                if isinstance(review, Review) and hasattr(review, 'place_id') and review.place_id == place_id]

    def get_reviews_by_user(self, user_id):
        """Get all reviews by a specific user"""
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews
                if isinstance(review, Review) and hasattr(review, 'user_id') and review.user_id == user_id]

    def update_review(self, review_id, update_data):
        """Update review with new data"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        review.update(update_data)
        return review

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")

        if hasattr(review, 'place_id'):
            place = self.place_repo.get(review.place_id)
            if place and hasattr(place, 'reviews') and review in place.reviews:
                place.reviews.remove(review)
                if USE_DATABASE:
                    from hbnb.app import db
                    db.session.commit()

        if hasattr(review, 'user_id'):
            user = self.user_repo.get(review.user_id)
            if user and hasattr(user, 'reviews') and user.reviews and review in user.reviews:
                user.reviews.remove(review)
                if USE_DATABASE:
                    from hbnb.app import db
                    db.session.commit()

        self.review_repo.delete(review_id)


# Singleton
facade = HBnBFacade()
