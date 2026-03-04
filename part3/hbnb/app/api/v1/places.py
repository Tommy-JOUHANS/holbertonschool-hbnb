"""
Place API endpoints.
Handles CRUD operations (no DELETE in Part 2).
Includes review retrieval for a place.
"""

from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

""" Namespace for place-related endpoints. """
api = Namespace("places", description="Place operations")


""" Model for creating/updating places. All fields required for creation, optional for updates. """
place_model = api.model("Place", {
    "title": fields.String(required=True),
    "description": fields.String(required=True),
    "price": fields.Float(required=True),
    "latitude": fields.Float(required=True),
    "longitude": fields.Float(required=True),
    "owner_id": fields.String(required=True)
})

""" Separate model for updates to allow partial updates (no required fields) """
place_update_model = api.model("PlaceUpdate", {
    "title": fields.String(),
    "description": fields.String(),
    "price": fields.Float(),
    "latitude": fields.Float(),
    "longitude": fields.Float()
})

@api.route("/")
class PlaceList(Resource):

    @api.expect(place_model, validate=True)
    @api.response(201, "Place created")
    @api.response(400, "Invalid input")
    def post(self):
        """Create place"""
        try:
            place = facade.create_place(api.payload)
            return place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, "Places retrieved")
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200


@api.route("/<string:place_id>")
class PlaceResource(Resource):

    @api.response(200, "Place retrieved")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, "Place updated")
    @api.response(404, "Place not found")
    def put(self, place_id):
        """Update place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        place.update(api.payload)
        return {"message": "Place updated successfully"}, 200


@api.route("/<string:place_id>/reviews")
class PlaceReviewList(Resource):

    @api.response(200, "Reviews retrieved")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return [r.to_dict() for r in place.reviews], 200

@api.route("/<string:place_id>/amenities/<string:amenity_id>")
class PlaceAmenityResource(Resource):

    @api.response(200, "Amenity added to place")
    @api.response(404, "Place or Amenity not found")
    def post(self, place_id, amenity_id):
        """Add amenity to a specific place"""
        try:
            place = facade.add_amenity_to_place(place_id, amenity_id)
            return place.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 404
