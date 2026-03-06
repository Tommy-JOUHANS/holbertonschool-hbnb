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
        """
        Get user by email address.
        
        Args:
            email (str): User's email address
            
        Returns:
            User: User object if found, None otherwise
        """
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
        place.add_amenities(amenity)
        
        # Commit via repository if using SQLAlchemy
        if USE_DATABASE:
            self.place_repo.update(place_id, {})  # empty dict just to commit changes
        
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
        
        # Create review and associate with place
        review = Review(**review_data)
        
        # Link review to place and add to place's reviews list
        self.review_repo.add(review)
        
        if hasattr(place, 'add_review'):
            place.add_review(review)
        
        if hasattr(user, 'reviews'):
            if not hasattr(user, 'reviews') or user.reviews is None:
                user.reviews = []
            user.reviews.append(review)
        
        # Commit relationships if using SQLAlchemy
        if USE_DATABASE:
            self.place_repo.update(place.id, {})
            self.user_repo.update(user.id, {})
        
        return review
    
    def get_review(self, review_id):
        """Get review by ID"""
        return self.review_repo.get(review_id)
    
    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        """
        Get all reviews for a specific place.
        
        Args:
            place_id (str): Place ID
            
        Returns:
            list: List of Review objects for the specified place
        """
        # ✅ CORRIGÉ: Filtrer seulement les Reviews qui ont place_id
        all_reviews = self.review_repo.get_all()
        return [review for review in all_reviews 
                if isinstance(review, Review) and hasattr(review, 'place_id') and review.place_id == place_id]
    
    # ✅ NOUVELLE MÉTHODE: Ajouter pour obtenir les reviews d'un utilisateur
    def get_reviews_by_user(self, user_id):
        """
        Get all reviews by a specific user.
        
        Args:
            user_id (str): User ID
            
        Returns:
            list: List of Review objects by the specified user
        """
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
        
        # Also remove review from associated place
        if hasattr(review, 'place_id'):
            place = self.place_repo.get(review.place_id)
            if place and hasattr(place, 'reviews') and review in place.reviews:
                place.reviews.remove(review)
                if USE_DATABASE:
                    self.place_repo.update(place.id, {})
        
        # Also remove review from associated user
        if hasattr(review, 'user_id'):
            user = self.user_repo.get(review.user_id)
            if user and hasattr(user, 'reviews') and user.reviews and review in user.reviews:
                user.reviews.remove(review)
                if USE_DATABASE:
                    self.user_repo.update(user.id, {})
        
        # Finally, delete review from repository
        self.review_repo.delete(review_id)


# Create a singleton instance of the facade
facade = HBnBFacade()
