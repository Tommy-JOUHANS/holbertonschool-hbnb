"""
User API endpoints.
Handles CRUD operations for users.
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
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

# Model for updates
user_update_model = api.model("UserUpdate", {
    "first_name": fields.String(description='First name of the user'),
    "last_name": fields.String(description='Last name of the user'),
    "email": fields.String(description='Email address (admin only)'),
    "password": fields.String(description='User password (admin only)')
})


@api.route("/")
class UserList(Resource):
    """
    Handles user collection operations.
    """
    
    @api.expect(user_model, validate=True)
    @api.response(201, "User created")
    @api.response(403, "Admin privileges required")
    @jwt_required()
    def post(self):
        """Create a new user (Admin only)"""
        current_user = get_jwt()
        
        # Check if user is admin
        if not current_user.get('is_admin', False):
            return {"error": "Admin privileges required"}, 403
        
        try:
            payload = api.payload
            
            # Check if email already exists
            if facade.get_user_by_email(payload["email"]):
                return {"error": "Email already registered"}, 400
            
            # Hash the password before storing
            payload["password"] = hash_password(payload["password"])
            
            user = facade.create_user(payload)
            return {
                "id": user.id,
                "message": "User successfully created"
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400
    
    @api.response(200, "Users retrieved")
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
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, "User not found")
        user_data = user.to_dict()
        # Remove password from response
        user_data.pop("password", None)
        return user_data, 200
    
    @api.expect(user_update_model, validate=True)
    @api.response(200, "User updated")
    @api.response(403, "Unauthorized action")
    @api.response(404, "User not found")
    @jwt_required()
    def put(self, user_id):
        """Update user (Users can update themselves, admins can update anyone)"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        # Regular users can only update themselves
        if not is_admin and current_user_id != user_id:
            return {"error": "Unauthorized action"}, 403
        
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        
        update_data = api.payload
        
        # Only admins can modify email and password
        if not is_admin:
            if 'email' in update_data or 'password' in update_data:
                return {"error": "You cannot modify email or password"}, 400
        else:
            # Admin is modifying email - check uniqueness
            if 'email' in update_data:
                existing_user = facade.get_user_by_email(update_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {"error": "Email already in use"}, 400
            
            # Hash password if being updated
            if 'password' in update_data:
                update_data['password'] = hash_password(update_data['password'])
        
        try:
            user.update(update_data)
            return user.to_dict(), 200
        except ValueError as e:
            return {"error": str(e)}, 400
