from flask_restful import Api
from app.resources.users_resource import UsersResource

def register_api_routes(app):
    api = Api(app)

    # Register the resource routes
    api.add_resource(UsersResource, '/users', '/users/<int:user_id>')
