from flask_restful import Api
from app.resources.users_resource import UsersResource
from app.resources.posts_resource import PostsResource

def register_api_routes(app):
    api = Api(app)

    # Register the resource routes
    api.add_resource(UsersResource, '/users', '/users/<int:user_id>')
    api.add_resource(PostsResource, '/posts', '/posts/<int:post_id>')
