from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Game:

    def __init__(self, data):
        self.id = data['id']
        self.game_name = data['game_name']
        self.game_type = data['game_type']
        self.game_description = data['game_description']
        self.game_image = data['game_image']
        self.host = data['host']
        self.alt_host = data['alt_host']
        self.player_amount = data['player_amount']
        self.game_location = data['game_location']
        self.game_date = data['game_date']
        self.game_time = data['game_time']  # Added game_time field
        self.game_night_description = data['game_night_description']  # Added game_night_description field
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.players = []

    @classmethod
    def save_game(cls,data):
        query = "INSERT INTO games (game_name,game_type,game_description,game_image) VALUES (%(game_name)s,%(game_type)s,%(game_description)s,%(game_image)s);"
        return connectToMySQL("Game_Night_Schema").query_db(query,data)
        
    @classmethod
    def save_game_night(cls, data):
        query = "INSERT INTO games (host, alt_host, player_amount, game_location, game_date) VALUES (%(host)s, %(alt_host)s, %(player_amount)s, %(game_location)s, %(game_date)s);"
        return connectToMySQL("Game_Night_Schema").query_db(query, data)
    
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
        if len(game['game_description']) < 2:
            flash("Description must be at least 2 characters",)
            is_valid= False
        # we can use a default image if none is supplied
        return is_valid
    
    @staticmethod
    def validate_game_night(game):
        is_valid = True
        if len(game['host']) < 2:
            flash("Host name must be at least 2 characters")
            is_valid = False
        if len(game['alt_host']) < 2:
            flash("Alternate host name must be at least 2 characters")
            is_valid = False
        if int(game['player_amount']) < 1:
            flash("Must have at least 1 player at the game night")
            is_valid = False
        if len(game['game_location']) < 2:
            flash("Location must be at least 2 characters")
            is_valid = False
        if len(game['game_date']) < 2:
            flash("A date for the game night must be provided")
            is_valid = False
        return is_valid    
    
    @classmethod
    def delete(cls,data):
        query  = "DELETE FROM games WHERE id = %(id)s;"
        
        return connectToMySQL("Game_Night_Schema").query_db(query, data)

    @classmethod
    def update(cls,data):
        query = "UPDATE games SET game_name=%(game_name)s, game_type=%(game_type)s, Host=%(Host)s, player_amount=%(player_amount)s, game_location=%(game_location)s, game_date=%(game_date)s,updated_at = NOW(), created_at = Now() WHERE id = %(id)s;"
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
                'user_location' : user_d['user_location'],
                'user_description' : user_d['user_description'],
                'user_image' : user_d['user_image'],
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
                'user_location' : user_d['user_location'],
                'user_description' : user_d['user_description'],
                'user_image' : user_d['user_image'],
                'password' : user_d['password'],
                'created_at' : user_d['users.created_at'],
                'updated_at' : user_d['users.updated_at']
                
                }
        
                user_object = user.User(new_user_d)
                game_object.creator = user_object
                game_object_list.append(game_object)
            return game_object_list