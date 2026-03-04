"""
Place API endpoints.
Handles CRUD operations for places.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.app.services import facade

api = Namespace('places', description='Place operations')

# Model for creating a place
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})

# Model for updating a place (all fields optional)
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place')
})


@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    def get(self):
        """Get all places (Public endpoint)"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200
    
    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new place (Authenticated users only)"""
        current_user = get_jwt_identity()
        place_data = api.payload
        
        # Set the owner_id to the current authenticated user
        place_data['owner_id'] = current_user
        
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        """Get place by ID (Public endpoint)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return place.to_dict(), 200
    
    @api.doc('update_place')
    @api.expect(place_update_model, validate=True)
    @jwt_required()
    def put(self, place_id):
        """Update a place (Owner only)"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        # Check if the current user is the owner
        if place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403
        
        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
