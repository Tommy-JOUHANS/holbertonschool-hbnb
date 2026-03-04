"""
User API endpoints.
Handles CRUD operations for users.
DELETE is not implemented in Part 2.
"""

from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

""" Namespace for user-related endpoints. """
api = Namespace("users", description="User operations")


""" Model for creating/updating users. All fields required for creation, optional for updates. """
user_model = api.model("User", {
    'id': fields.String(readOnly=True, description="User ID"),
    "first_name": fields.String(required=True, description='First name of the user'),
    "last_name": fields.String(required=True, description='Last name of the user'),
    "email": fields.String(required=True, description='Email address of the user')
})
""" Separate model for updates to allow partial updates (no required fields) """
user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(),
    "last_name": fields.String(),
    "email": fields.String()
})

""" Model for error responses. """
error_model = api.model("Error", {
    "error": fields.String(description="Error message")
})

@api.route("/")
class UserList(Resource):
    """
    Handles user collection operations.
    """

    @api.expect(user_model, validate=True)
    @api.response(201, "User created", user_model)
    @api.response(400, "Invalid input data", error_model)
    def post(self):
        """Create a new user"""
        try:
            user = facade.create_user(api.payload)
            return user.to_dict(), 201
        except ValueError as e:
            if "already exists" in str(e):
                return {"error": str(e)}, 409
            return {"error": str(e)}, 400

    @api.response(200, "Users retrieved")
    @api.marshal_with(user_model, skip_none=True)
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200


@api.route("/<string:user_id>")
class UserResource(Resource):
    """
    Handles single user operations.
    """

    @api.response(200, "User retrieved")
    @api.response(404, "User not found")
    @api.marshal_with(user_model, skip_none=True)
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404,"User not found"),
        return user.to_dict(), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, "User updated")
    @api.response(404, "User not found")
    @api.marshal_with(user_model, skip_none=True)
    def put(self, user_id):
        """Update user"""
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        try:
           user.update(api.payload)
           return user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
