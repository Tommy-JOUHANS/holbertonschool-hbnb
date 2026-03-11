"""
Amenity API endpoints.
Handles CRUD operations (no DELETE in Part 2).
"""

from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

api = Namespace("amenities", description="Amenity operations")



amenity_model = api.model("Amenity", {
    "id": fields.String(),
    "name": fields.String(required=True),
    "description": fields.String()
})


@api.route("/")
class AmenityList(Resource):
    """
    Handles amenity collection operations.
    """

    @api.expect(amenity_model, validate=True)
    @api.response(201, "Amenity created")
    @api.response(400, "Invalid input")
    @api.marshal_with(amenity_model, skip_none=True)
    def post(self):
        """Create amenity"""
        try:
            amenity = facade.create_amenity(api.payload)
            return amenity.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, "Amenities retrieved")
    @api.marshal_with(amenity_model, skip_none=True)
    def get(self):
        """Get all amenities"""
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route("/<string:amenity_id>")
class AmenityResource(Resource):
    """
    Handles single amenity operations.
    """

    @api.response(200, "Amenity retrieved")
    @api.response(404, "Amenity not found")
    @api.marshal_with(amenity_model, skip_none=True)
    def get(self, amenity_id):
        """Get amenity by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return amenity.to_dict(), 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, "Amenity updated")
    @api.response(404, "Amenity not found")
    @api.marshal_with(amenity_model, skip_none=True)
    def put(self, amenity_id):
        """Update amenity"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        amenity.update(api.payload)
        return amenity.to_dict(), 200
    