from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user




class Rating:

    def __init__(self,data):
        self.id = data['id']
        self.rating = data['rating']
        self.user_id = data['user_id']
        self.game_id = data['game_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.sender = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO ratings (rating,user_id,game_id,) VALUES (%(rating)s,%(user_id)s,%(game_id)s);"
        return connectToMySQL("Game_Night_Schema").query_db(query,data)
    
    @classmethod
    def get_all_join_user(cls,data): # no data needed since grabbing all
        query = "SELECT * FROM ratings JOIN users on ratings.user_id = users.id WHERE ratings.game_id = %(id)s;"
        results = connectToMySQL("Game_Night_Schema").query_db(query,data)
        if len(results) == 0:
            return []
        else:
            # 
            rating_object_list = []
            for user_d in results:
                print(user_d)
            
                rating_object = cls(user_d)
                new_user_d = {
                'id' : user_d ['users.id'],
                'first_name': user_d['first_name'],
                'last_name' : user_d['last_name'],
                'email': user_d['email'],
                'phone_number' : user_d['phone_number'],
                'user_location' : user_d['user_location'],
                'user_description' : user_d['user_description'],
                'user_image' : user_d['user_image'],
                'password' : user_d['password'],
                'created_at' : user_d['users.created_at'],
                'updated_at' : user_d['users.updated_at']
                
                }
        
                user_object = user.User(new_user_d)
                rating_object.sender = user_object
                rating_object_list.append(rating_object)
            return rating_object_list