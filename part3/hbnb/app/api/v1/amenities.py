"""
Amenity API endpoints.
Handles CRUD operations for amenities.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from hbnb.app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Model for amenity
amenity_model = api.model('Amenity', {
    'id': fields.String(readOnly=True, description='Amenity ID'),
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.doc('list_amenities')
    def get(self):
        """Get all amenities (Public)"""
        amenities = facade.get_all_amenities()
        return [amenity.to_dict() for amenity in amenities], 200
    
    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @jwt_required()
    def post(self):
        """Create a new amenity (Admin only)"""
        current_user = get_jwt()
        
        # Check if user is admin
        if not current_user.get('is_admin', False):
            return {"error": "Admin privileges required"}, 403
        
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.doc('get_amenity')
    def get(self, amenity_id):
        """Get amenity by ID (Public)"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return amenity.to_dict(), 200
    
    @api.doc('update_amenity')
    @api.expect(amenity_model, validate=True)
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity (Admin only)"""
        current_user = get_jwt()
        
        # Check if user is admin
        if not current_user.get('is_admin', False):
            return {"error": "Admin privileges required"}, 403
        
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        try:
            amenity.update(api.payload)
            return amenity.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400
