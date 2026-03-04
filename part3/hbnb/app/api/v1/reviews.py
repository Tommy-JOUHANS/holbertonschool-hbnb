"""
Review API endpoints.
Full CRUD including DELETE.
"""

from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

api = Namespace("reviews", description="Review operations")


"""Model for creating/updating reviews. All fields required for creation, optional for updates."""
review_model = api.model("Review", {
    "text": fields.String(required=True),
    "rating": fields.Float(required=True),
    "user_id": fields.String(required=True),
    "place_id": fields.String(required=True)
})

"""Separate model for updates to allow partial updates (no required fields)"""
review_update_model = api.model("ReviewUpdate", {
    "text": fields.String(),
    "rating": fields.Float()
})

@api.route("/")
class ReviewList(Resource):

    @api.expect(review_model, validate=True)
    @api.response(201, "Review created")
    @api.response(400, "Invalid input")
    def post(self):
        """Create review"""
        try:
            review = facade.create_review(api.payload)
            return review.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, "Reviews retrieved")
    def get(self):
        """Get all reviews"""
        reviews = facade.review_repo.get_all()
        return [r.to_dict() for r in reviews], 200


@api.route("/<string:review_id>")
class ReviewResource(Resource):

    @api.response(200, "Review retrieved")
    @api.response(404, "Review not found")
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, "Review updated")
    @api.response(404, "Review not found")
    def put(self, review_id):
        """Update review"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        review.update(api.payload)
        return {"message": "Review updated successfully"}, 200

    @api.response(200, "Review deleted")
    @api.response(404, "Review not found")
    def delete(self, review_id):
        """Delete review"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
