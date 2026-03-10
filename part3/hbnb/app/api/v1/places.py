"""
Place API endpoints.
Handles CRUD operations for places.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from hbnb.app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(description="Id of user")
})

place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(required=True, description="ID of user")
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
        """Update a place (Owner or Admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.doc('delete_place')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (Owner or Admin only)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403
        try:
            facade.delete_place(place_id)
            return {'message': 'Place deleted successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

# =========================================================================
# AMENITIES D'UNE PLACE
# =========================================================================

@api.route('/<place_id>/amenities')
class PlaceAmenities(Resource):
    @api.doc('get_place_amenities')
    def get(self, place_id):
        """Récupérer les amenities d'une place (Public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        return [a.to_dict() for a in place.amenities], 200

@api.route('/<place_id>/amenities/<amenity_id>')
class PlaceAmenityResource(Resource):
    @api.doc('add_amenity_to_place')
    @jwt_required()
    def post(self, place_id, amenity_id):
        """Lier une amenity à une place (Owner ou Admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        if amenity in place.amenities:
            return {'error': 'Amenity already linked to this place'}, 400

        try:
            place.amenities.append(amenity)
            facade.save()
            return {'message': 'Amenity added to place successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

    @api.doc('remove_amenity_from_place')
    @jwt_required()
    def delete(self, place_id, amenity_id):
        """Retirer une amenity d'une place (Owner ou Admin)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        if amenity not in place.amenities:
            return {'error': 'Amenity not linked to this place'}, 400

        try:
            place.amenities.remove(amenity)
            facade.save()
            return {'message': 'Amenity removed from place successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 500

# =========================================================================
# REVIEWS D'UNE PLACE
# =========================================================================

@api.route('/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.doc('get_place_reviews')
    def get(self, place_id):
        """Récupérer les reviews d'une place (Public)"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        # ✅ Utiliser facade.get_reviews_by_place() au lieu de place.reviews
        reviews = facade.get_reviews_by_place(place_id)
        return [r.to_dict() for r in reviews], 200
