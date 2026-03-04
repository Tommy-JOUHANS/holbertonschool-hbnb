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
            # SQLAlchemy repositories (will be used after model mapping)
            self.user_repo = RepositoryClass(User)
            self.place_repo = RepositoryClass(Place)
            self.review_repo = RepositoryClass(Review)
            self.amenity_repo = RepositoryClass(Amenity)
        else:
            # In-memory repositories
            self.user_repo = RepositoryClass()
            self.place_repo = RepositoryClass()
            self.review_repo = RepositoryClass()
            self.amenity_repo = RepositoryClass()
    
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
    
    def get_user_by_email(self, email):
        """
        Get user by email address.
        
        Args:
            email (str): User's email address
            
        Returns:
            User: User object if found, None otherwise
        """
        return self.user_repo.get_by_attribute("email", email)
    
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
    
    def update_place(self, place_id, update_data):
        """Update place with new data"""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        place.update(update_data)
        return place
    
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
        
        """Create review and associate with place"""
        review = Review(**review_data)
        
        """Link review to place and add to place's reviews list"""
        self.review_repo.add(review)
        
        place.add_review(review)
        
        user.reviews.append(review)
        
        return review
    
    def get_review(self, review_id):
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """
        Get all reviews for a specific place.
        
        Args:
            place_id (str): Place ID
            
        Returns:
            list: List of Review objects for the specified place
        """
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews if review.place_id == place_id]
    
    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found")
        
        """Also remove review from associated place"""
        place = review.place
        if place and review in place.reviews:
            place.reviews.remove(review)
        
        """Finally, delete review from repository"""
        self.review_repo.delete(review_id)
