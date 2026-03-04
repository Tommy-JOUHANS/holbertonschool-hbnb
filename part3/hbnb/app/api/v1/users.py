"""
User API endpoints.
Handles CRUD operations for users.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.app.services import facade
from hbnb.app.utils import hash_password

api = Namespace("users", description="User operations")

# Model for creating users
user_model = api.model("User", {
    'id': fields.String(readOnly=True, description="User ID"),
    "first_name": fields.String(required=True, description='First name of the user'),
    "last_name": fields.String(required=True, description='Last name of the user'),
    "email": fields.String(required=True, description='Email address of the user'),
    "password": fields.String(required=True, description='User password'),
    "is_admin": fields.Boolean(description='Is user an admin', default=False)
})

# Model for updates (excluding email and password)
user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(description='First name of the user'),
    "last_name": fields.String(description='Last name of the user')
})

# Model for error responses
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
            payload = api.payload
            # Hash the password before storing
            payload["password"] = hash_password(payload["password"])
            user = facade.create_user(payload)
            return {
                "id": user.id,
                "message": "User successfully created"
            }, 201
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
            api.abort(404, "User not found")
        user_data = user.to_dict()
        # Remove password from response if present
        user_data.pop("password", None)
        return user_data, 200
    
    @api.expect(user_update_model, validate=True)
    @api.response(200, "User updated")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    @jwt_required()
    def put(self, user_id):
        """Update user (Users can only update their own information)"""
        current_user = get_jwt_identity()
        
        # Check if user is trying to update their own profile
        if current_user != user_id:
            return {"error": "Unauthorized action"}, 403
        
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        # Check if trying to modify email or password
        update_data = api.payload
        if 'email' in update_data or 'password' in update_data:
            return {"error": "You cannot modify email or password"}, 400
        
        try:
            user.update(update_data)
            return user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
