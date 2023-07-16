from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_app.models.purchase import Purchase

@app.route('/purchase/car/<int:car_id>')
def purchase(car_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'car_id': car_id,
        'user_id':session['user_id']
    }
    Purchase.add_purchase(data)
    return redirect('/dashboard')

@app.route('/purchase/history')
def purchase_history():
    if 'user_id' not in session:
        return redirect('/logout')
    user = User.get_user_by_id({'id': session['user_id']})
    user_purchases = Purchase.get_purchases_by_user_id({'id':session['user_id']})
    cars_bought = []
    for purchase in user_purchases:
        car = Car.get_car_by_id({'id': purchase.car_id})
        cars_bought.append(car)
    return render_template('user_purchases.html', user=user, cars_bought=cars_bought)