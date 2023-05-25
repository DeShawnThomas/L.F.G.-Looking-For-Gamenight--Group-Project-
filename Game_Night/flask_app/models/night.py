from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash



class Night:

    db = "game_night_schema"

    def __init__(self, data):
        self.id = data['id']
        self.host = data['host']
        self.alt_host = data['alt_host']
        self.player_amount = data['player_amount']
        self.game_location = data['game_location']
        self.game_date = data['game_date']
        self.game_time = data['game_time']
        self.night_description = data['night_description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save_night(cls, data):
        query = "INSERT INTO nights (host, alt_host, player_amount, game_location, game_date, game_time, night_description, user_id) VALUES (%(host)s, %(alt_host)s, %(player_amount)s, %(game_location)s, %(game_date)s, %(game_time)s, %(night_description)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_night(night):
        is_valid = True

        if len(night['host']) < 2:
            flash("Host name must be at least 2 characters")
            is_valid = False
        if len(night['alt_host']) < 2:
            flash("Alternate host name must be at least 2 characters")
            is_valid = False
        if int(night['player_amount']) < 1:
            flash("Must have at least 1 player at the game night")
            is_valid = False
        if len(night['game_location']) < 2:
            flash("Location must be at least 2 characters")
            is_valid = False
        if (night['game_date']) == "":
            flash("A date for the game night must be provided")
            is_valid = False
        if (night['game_time']) == "":
            flash("A time for the game night must be provided")
            is_valid = False
        if len(night['night_description']) < 2:
            flash("Description must be at least 2 characters")
            is_valid = False
        return is_valid

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM nights WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE nights SET host = %(host)s, alt_host = %(alt_host)s, player_amount = %(player_amount)s, game_location = %(game_location)s, game_date = %(game_date)s, game_time = %(game_time)s, night_description = %(night_description)s, user_id = %(user_id)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM nights JOIN users ON nights.user_id = users.id WHERE nights.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) == 0:
            return None
        else:
            user_d = results[0]
            night_object = cls(user_d)
            new_user_d = {
                'id': user_d['users.id'],
                'first_name': user_d['first_name'],
                'last_name': user_d['last_name'],
                'email': user_d['email'],
                'phone_number': user_d['phone_number'],
                'user_location': user_d['user_location'],
                'user_description': user_d['user_description'],
                'user_image': user_d['user_image'],
                'password': user_d['password'],
                'created_at': user_d['users.created_at'],
                'updated_at': user_d['users.updated_at']
            }
            user_object = User(new_user_d)
            night_object.creator = user_object
            return night_object

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM nights JOIN users ON nights.user_id = users.id;"
        results = connectToMySQL(cls.db).query_db(query)
        night_object_list = []
        for user_d in results:
            night_object = cls(user_d)
            new_user_d = {
                'id': user_d['users.id'],
                'first_name': user_d['first_name'],
                'last_name': user_d['last_name'],
                'email': user_d['email'],
                'phone_number': user_d['phone_number'],
                'user_location': user_d['user_location'],
                'user_description': user_d['user_description'],
                'user_image': user_d['user_image'],
                'password': user_d['password'],
                'created_at': user_d['users.created_at'],
                'updated_at': user_d['users.updated_at']
            }
            user_object = User(new_user_d)
            night_object.creator = user_object
            night_object_list.append(night_object)
        return night_object_list
