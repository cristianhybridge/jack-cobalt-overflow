from flask import request
from flask_restful import Resource
from app.models.posts_entity import db, Posts

class PostsResource(Resource):
    def get_all(self):
        all_posts = Posts.query.all()

        list = [
            {
                "post_id": post.post_id,
                "created_by": post.created_by,
                "creator" : post.creator.username,
                "title": post.title,
                "commentary": post.commentary,
                "affected_area": post.affected_area,
                "priority": post.priority,
                "creation_date": post.creation_date.isoformat(),
                "expiration_date": post.expiration_date.isoformat()                
            } for post in all_posts
        ]

        print(f"PostsResource/GetAll: {list}")

        return list, 200

    # def post(self):
    #     data = request.get_json()
    #     new_user = User(username=data['username'], email=data['email'])
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return {"message": "User created successfully"}, 201