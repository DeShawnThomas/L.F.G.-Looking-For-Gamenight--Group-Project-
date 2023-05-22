from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user



class Game:

    def __init__(self,data):
        self.id = data['id']
        self.game_name = data['game_name']
        self.game_type = data['game_type']
        self.G_description = data['G_description']
        self.G_image = data['G_image']
        self.Host = data['Host']
        self.player_amount = data['player_amount']
        self.G_location = data['G_location']
        self.G_date = data['G_date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        

    @classmethod
    def save(cls,data):
        query = "INSERT INTO games (game_name,game_type,G_description,G_image,Host,player_amount,G_location,G_date,created_at,updated_at) VALUES (%(game_name)s,%(game_type)s,%(G_description)s,%(G_image)s,%(Host)s,%(player_amount)s,%(G_location)s,%(G_date)s,Now(),Now());"
        return connectToMySQL("Game_Night_Schema").query_db(query,data)
    
    @staticmethod
    def validate_game(game):
        is_valid = True
        query = "SELECT * FROM games;"
        results = connectToMySQL("Game_Night_Schema").query_db(query,game)
        if len(game['game_name']) < 2:
            flash("Game name must be at least 2 characters",)
            is_valid= False
        if len(game['game_type']) < 2:
            flash("Game type must be at least 2 characters",)
            is_valid= False
        if len(game['G_location']) < 2:
            flash("Location must be at least 2 characters",)
            is_valid= False
        if len(game['G_description']) < 2:
            flash("Description must be at least 2 characters",)
            is_valid= False
        
        return is_valid
    
    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM games WHERE id = %(id)s;"
        
        return connectToMySQL("Game_Night_Schema").query_db(query, data)

    @classmethod
    def update(cls,data):
        query = "UPDATE games SET game_name=%(game_name)s, game_typet=%(game_type)s, Host=%(Host)s, player_amount=%(player_amount)s, G_location=%(G_location)s, G_date=%(G_date)s,updated_at = NOW(), created_at = Now() WHERE id = %(id)s;"
        return connectToMySQL("Game_Night_Schema").query_db(query,data)

    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM games Join users on games.user_id = users.id Where games.id = %(id)s;"
        results = connectToMySQL("Game_Night_Schema").query_db(query,data)
        if len(results) == 0:
            return None
        else:
            # data = {'id':id}
            user_d = results[0]
            game_object = cls(user_d)
            new_user_d = {
                'id' : user_d ['users.id'],
                'first_name': user_d['first_name'],
                'last_name' : user_d['last_name'],
                'email': user_d['email'],
                'phone_number' : user_d['phone_number'],
                'U_location' : user_d['U_location'],
                'U_description' : user_d['U_description'],
                'U_image' : user_d['U_image'],
                'password' : user_d['password'],
                'created_at' : user_d['users.created_at'],
                'updated_at' : user_d['users.updated_at']
             }
        
            user_object = user.User(new_user_d)
            game_object.creator = user_object
       
            # return cls(results[0])
        return game_object
    
    @classmethod
    def get_all(cls): # no data needed since grabbing all
        query = "SELECT * FROM games Join users on games.user_id = users.id;"
        results = connectToMySQL("Game_Night_Schema").query_db(query)
        if len(results) == 0:
            return []
        else:
            # 
            game_object_list = []
            for user_d in results:
                print(user_d)
            
                game_object = cls(user_d)
                new_user_d = {
                     'id' : user_d ['users.id'],
                'first_name': user_d['first_name'],
                'last_name' : user_d['last_name'],
                'email': user_d['email'],
                'phone_number' : user_d['phone_number'],
                'U_location' : user_d['U_location'],
                'U_description' : user_d['U_description'],
                'U_image' : user_d['U_image'],
                'password' : user_d['password'],
                'created_at' : user_d['users.created_at'],
                'updated_at' : user_d['users.updated_at']
                
                }
        
                user_object = user.User(new_user_d)
                game_object.creator = user_object
                game_object_list.append(game_object)
            return game_object_list