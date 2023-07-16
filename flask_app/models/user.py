from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    DB = 'cardealz_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.purchased_cars = [] #empty list so we can add purchases to a user account

    ############# Registration validation for users #############
    @staticmethod
    def validate_registration(user):
        is_valid = True
        if not user['first_name'] or not user['last_name'] or not user['email'] or not user['password'] or not user['confirm_pw']:
            flash("All fields must be filled!", "register_user")
            is_valid = False
            return is_valid #return here to avoid key errors below
        if len(user['first_name']) < 3: # first name validation
            flash("First name must be at least 3 characters!", "register_user")
            is_valid = False
        if len(user['last_name']) < 3: #last name validation
            flash("Last name must be at least 3 characters!", "register_user")
            is_valid = False
        if len(user['password']) < 8: #password validation
            flash("Password must be at least 8 characters!", "register_user")
            is_valid = False    
        if not re.match(EMAIL_REGEX, user['email']):
            flash("Invalid email!", "register_user")
            is_valid = False
        if user['password'] != user['confirm_pw']:
            flash("Passwords must match!","register_user")
            is_valid = False
        return is_valid
    
    ############# create new user #############
    @classmethod
    def create_user(cls, data):
        query = '''INSERT INTO users (first_name, last_name, password, email) 
                    VALUES (%(first_name)s, %(last_name)s, %(password)s, %(email)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    ############# read user methods #############
    @classmethod
    def get_user_by_email(cls, data):
        query = '''SELECT * FROM users WHERE users.email = %(email)s;'''
        user = connectToMySQL(cls.DB).query_db(query, data)
        print("DB RESPONSE: ", user)

        if len(user) < 1:
            return False
        return cls(user[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = '''SELECT * FROM users WHERE users.id = %(id)s;'''
        user = connectToMySQL(cls.DB).query_db(query, data)
        if len(user) < 1:
            return False
        return cls(user[0])
    