from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user #import user model file (not class to avoid circular imports)
from flask_app.models import car

########### creating a new 'Purchase' class for the 'purchases' table in the DB
# this will track all the user purchases
class Purchase:
    DB = 'cardealz_schema'
    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.car_id = data['car_id']
        self.purchase_date = data['purchase_date']
        self.car = None
        self.buyer = None

    @classmethod
    def get_all_purchases(cls):
        query = '''SELECT * FROM purchases;'''
        return connectToMySQL(cls.DB).query_db(query)

    @classmethod
    def add_purchase(cls, data):
        query = '''INSERT INTO purchases (user_id, car_id, purchase_date)
                VALUES (%(user_id)s, %(car_id)s, CURRENT_TIMESTAMP());'''
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_purchases_by_user_id(cls, data):
        query = '''SELECT * FROM purchases WHERE purchases.user_id = %(id)s'''
        results = connectToMySQL(cls.DB).query_db(query, data)
        all_purchases = []
        if not results:
            return all_purchases
        for result in results:
            purchased_car = car.Car.get_car_by_id({'id':result['car_id']}) # get car object with the car's id
            purchase = cls(result) #create Purchase object
            purchase.car = purchased_car #set the purchased car object to the value of the purchase.car attribute
            all_purchases.append(purchase)
        return all_purchases


