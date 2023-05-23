from flask_app.config.mysqlconnection import connectToMySQL
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash
from flask_app.models.game import Game

class User:

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.phone_number = data['phone_number']
        self.U_location = data['U_location']
        self.U_description = data['U_description']
        self.U_image = data['U_image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.games = []



    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password,phone_number,U_location,U_description,U_image) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(phone_number)s,%(U_location)s,%(U_description)s,%(U_image)s)"
        return connectToMySQL("Game_Night_Schema").query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, eamil=%(email)s, phone_number=%(phone_number)s, password=%(password)s, U_location=%(U_location)s, updated_at = NOW(), created_at = Now() WHERE id = %(id)s;"
        return connectToMySQL("moment_schema").query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL("Game_Night_Schema").query_db(query)
        users = []
        for row in results:
            users.append( cls(row))
        return users

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("Game_Night_Schema").query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL("Game_Night_Schema").query_db(query,data)
        data = {'id':id}
        return cls(results[0])
    
    
    @classmethod
    def get_one_game(cls, data ): 
        query = "SELECT * FROM users LEFT JOIN games on users.id = games.user_id WHERE users.id = %(id)s;" 
        results = connectToMySQL("Game_Night_Schema").query_db(query,data) 
        print(results)  
        User = cls(results[0])  
        for row in results: 
            game = { 
                'id': row['games.id'],
                'game_name': row['game_name'],
                'game_type': row['game_type'],
                'G_description': row['G_description'],
                'G_image': row['G_image'],
                'Host': row['Host'],
                'player_amount': row['player_amount'],
                'G_location': row['G_location'],
                'G_date': row['G_date'],
                'created_at': row['games.created_at'],
                'updated_at': row['games.updated_at']
            }
            User.games.append(Game(game))  
        return User









    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL("Game_Night_Schema").query_db(query,user)
        if len(results) >= 1:
            flash("Email unusable.","regError",)
            is_valid=False
        if not EMAIL_REGEX.match(user['email']):
            flash("Incorrect Email", "regError",)
            is_valid=False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters", "regError",)
            is_valid= False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", "regError")
            is_valid= False
        if len(user['phone_number']) < 2:
            flash("phone number must be at least 10 characters", "regError")
            is_valid= False
        if len(user['U_location']) < 2:
            flash("Location must be at least 2 characters", "regError")
            is_valid= False
        if len(user['password']) < 8:
            flash("Password must be no less then 8 characters", "regError")
            is_valid= False
        if user['password'] != user['verify']:
            flash("Passwords dont align","regError",)
        return is_valid

   