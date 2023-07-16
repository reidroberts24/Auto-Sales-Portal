from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_bcrypt import Bcrypt

############## render form to add new car ##############
@app.route('/post/car')
def post_car():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('add_car_for_sale.html')

############## add new car to postings ##############
@app.route('/add/car', methods=["POST"])
def add_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_car_info(request.form):
        return redirect('/post/car')
    data = {
        'make': request.form['make'],
        'model': request.form['model'],
        'price': request.form['price'],
        'year': request.form['year'],
        'description': request.form['description'],
        'user_id': session['user_id']
    }

    new_car_id = Car.create_car(data)
    return redirect('/dashboard')

############## show car's info on a card ##############
@app.route('/show/car/info/<int:car_id>')
def show_car_info(car_id):
    if 'user_id' not in session:
        return redirect('/logout')
    car = Car.get_car_by_id({'id':car_id})
    user = User.get_user_by_id({'id':session['user_id']})
    return render_template('car_info.html', car=car, user=user)



############## render form to edit car ##############
@app.route('/edit/form/<int:car_id>')
def render_edit_page(car_id):
    if 'user_id' not in session:
        return redirect('/logout')
    car = Car.get_car_by_id({'id':car_id})
    user = User.get_user_by_id({'id':session['user_id']})
    return render_template('edit_car.html', car=car, user=user)

############## render form to edit car ##############
@app.route('/edit/posting', methods=["POST"])
def update_posting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_car_info(request.form):
        return redirect(f"/edit/form/{request.form['id']}")
    data = {
        'id': request.form['id'],
        'price': request.form['price'],
        'model': request.form['model'],
        'make': request.form['make'],
        'year': request.form['year'],
        'description': request.form['description']
    }
    Car.edit_car(data)
    return redirect('/dashboard')

############## render form to edit car ##############
@app.route('/delete/posting/<int:car_id>')
def delete_posting(car_id):
    if 'user_id' not in session:
        return redirect('/logout')
    Car.delete({'id':car_id})
    return redirect('/dashboard')
