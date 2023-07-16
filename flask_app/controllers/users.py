from flask_app import app
from flask import Flask, render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.car import Car
from flask_app.models.purchase import Purchase
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

############# main login page #############
@app.route('/')
def root():
    return render_template('register_login.html')

############# register new user #############
@app.route('/register', methods=["POST"])
def register_user():
    if not User.validate_registration(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    new_user_id = User.create_user(data)
    session['user_id'] = new_user_id
    return redirect('/dashboard')

############# login existing user #############
@app.route('/login', methods=["POST"])
def login():
    user = User.get_user_by_email({'email':request.form['email']})
    if not user:
        flash("Invalid email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

############# user dashboard #############
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_cars_for_sale = Car.get_all_cars()
    user = User.get_user_by_id(data)
    return render_template('user_dashboard.html', cars=all_cars_for_sale, user=user)



############# user logout #############
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
