from flask import request
from flask_restful import Resource
from app.models.posts_entity import db, Posts

class PostsResource(Resource):
    def get(self):
        all_posts = Posts.query.all()

        users_list = [
            {
                "post_id": post.post_id,
                "title": post.title,
                "commentary": post.commentary,
                "created_by": post.created_by,
            } for post in all_posts
        ]

        print(f"PostsResource/GetAll: {users_list}")

        return users_list, 200

    # def post(self):
    #     data = request.get_json()
    #     new_user = User(username=data['username'], email=data['email'])
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return {"message": "User created successfully"}, 201