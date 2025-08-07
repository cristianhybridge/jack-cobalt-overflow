from flask import request
from flask_restful import Resource
from app.models.users_entity import db, Users

class UsersResource(Resource):
    def get(self):
        all_users = Users.query.all()

        users_list = [
            {
                "user_id": user.user_id,
                "username": user.username,
                "nickname": user.nickname
            } for user in all_users
        ]
        
        print(f"UsersResource/GetAll: {users_list}")
        
        return users_list, 200
    
    # def post(self):
    #     data = request.get_json()
    #     new_user = User(username=data['username'], email=data['email'])
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return {"message": "User created successfully"}, 201