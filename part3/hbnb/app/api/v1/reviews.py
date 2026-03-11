"""
Review API endpoints.
Handles CRUD operations for reviews.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from hbnb.app.services import facade

api = Namespace('reviews', description='Review operations')

# Model for creating a review
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Model for updating a review
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)')
})


@api.route('/')
class ReviewList(Resource):
    @api.doc('list_reviews')
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200
    
    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new review (Authenticated users only)"""
        current_user = get_jwt_identity()
        review_data = api.payload
        
        # Get the place
        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Check if user is trying to review their own place
        if place.owner_id == current_user:
            return {'error': 'You cannot review your own place'}, 400
        
        # Check if user has already reviewed this place
        existing_reviews = facade.get_reviews_by_place(review_data['place_id'])
        for review in existing_reviews:
            if review.user_id == current_user:
                return {'error': 'You have already reviewed this place'}, 400
        
        # Set the user_id to the current authenticated user
        review_data['user_id'] = current_user
        
        try:
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.doc('get_review')
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200
    
    @api.doc('update_review')
    @api.expect(review_update_model, validate=True)
    @jwt_required()
    def put(self, review_id):
        """Update a review (Author or Admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check if user is author or admin
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            review.update(api.payload)
            return review.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    @api.doc('delete_review')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (Author or Admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404
        
        # Check if user is author or admin
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
