from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user #import user model file (not class to avoid circular imports)
import re
from flask import flash


class Car:
    DB = 'cardealz_schema'
    def __init__(self, data):
        self.id = data['id']
        self.model = data['model']
        self.make = data['make']
        self.year = data['year']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.seller = None #add NoneType object to know who is selling the car
        self.purchase_id = None

    ############# Registration validation for cars #############
    @staticmethod
    def validate_car_info(car):
        is_valid = True
        if not car['model'] or not car['make'] or not car['year'] or not car['description'] or not car['price']:
            flash("All fields must be filled!", "register_car")
            is_valid = False
            return is_valid #return here to avoid key errors below
        if int(car['year']) <= 0:
            flash("Car's year must be greater than 0!", "register_car")
            is_valid = False
        if int(car['price']) <= 0:
            flash("Car's price must be greater than 0!", "register_car")
            is_valid = False
        return is_valid
    
    ############# create new car method #############
    @classmethod
    def create_car(cls, data):
        query = '''INSERT INTO cars (model, make, year, description, price, user_id) 
                    VALUES (%(model)s, %(make)s, %(year)s, %(description)s, %(price)s, %(user_id)s);'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    ############# read all cars method #############
    @classmethod
    def get_all_cars(cls):
        query = '''SELECT * FROM cars
                    JOIN users on cars.user_id = users.id
                    LEFT JOIN purchases ON cars.id = purchases.car_id;'''
        results = connectToMySQL(cls.DB).query_db(query)
        all_cars = []
        if results:
            for car in results:
                current_car = cls(car)
                if car['purchases.id']:
                    current_car.purchase_id = car['purchases.id']
                user_info = { #store user info from table join to add the User object to the car's seller
                    'id': car['users.id'],
                    'first_name': car['first_name'],
                    'last_name' : car['last_name'],
                    'password' : "",
                    'email' : car['email'],
                    'created_at' : car['users.created_at'],
                    'updated_at' : car['users.updated_at']
                }
                current_car.seller = user.User(user_info) #call model file then class
                all_cars.append(current_car)
        return all_cars

    ############# read car by id method #############
    @classmethod
    def get_car_by_id(cls, data):
        query = '''SELECT * FROM cars
                    JOIN users on cars.user_id = users.id
                    WHERE cars.id = %(id)s;'''
        result = connectToMySQL(cls.DB).query_db(query, data)
        if not result:
            return False
        result = result[0]
        car = cls(result)    
        user_info = { #store user info from table join to add the User object to the car's seller
            'id': result['users.id'],
            'first_name': result['first_name'],
            'last_name' : result['last_name'],
            'password' : "",
            'email' : result['email'],
            'created_at' : result['users.created_at'],
            'updated_at' : result['users.updated_at']
        }
        car.seller = user.User(user_info) #call model file then class
        return car
    
    ############# update car method #############
    @classmethod
    def edit_car(cls, data):
        query = '''UPDATE cars SET 
            make = %(make)s,
            model = %(model)s,
            year = %(year)s,
            description = %(description)s, 
            price = %(price)s,
            updated_at = CURRENT_TIMESTAMP()
            WHERE cars.id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    ############# delete car method (for when user purchases it) #############
    @classmethod
    def delete(cls, data):
        query = '''DELETE FROM cars WHERE cars.id = %(id)s;'''
        return connectToMySQL(cls.DB).query_db(query, data)