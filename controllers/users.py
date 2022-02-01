from flask_app import app
from flask_bcrypt import Bcrypt
from flask import render_template, redirect, request, session, flash
from ..models import recipe, user
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    session['first_name'] = request.form['first_name']

    user_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }

    user_id = user.User.save_user(user_data)
    session['user_id'] = user_id
    # print(f"user_id: {user_id}")
    return redirect('dashboard')

@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { 
        "email" : request.form["email"] 
        }
    user_in_db = user.User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')

    return redirect("/dashboard")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }

    logged_in_user=user.User.get_by_email(data)
    print(f"PRINT: {user.User.get_by_email(data)}")
    return render_template('dashboard.html', logged_in_user=logged_in_user,  all_recipes= recipe.Recipe.get_all_recipes() )