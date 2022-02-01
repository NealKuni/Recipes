from flask_app import app
from flask import render_template, redirect, request, session, flash
from ..models import user, recipe

@app.route('/recipes/<int:id>')
def show_users_recipe(id):
    
    return render_template('show_recipe.html', user_recipe = recipe.get_one_recipe(id))

@app.route('/recipes')
def create_recipes_page():
    return render_template('create_new_recipe.html')

@app.route('/recipes/new', methods=['POST'])
def create_recipes():

    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date": request.form['date'],
        "under_30": request.form['under_30'],
        "user_id": session['user_id']
    }
    print(f'dict: {data}')
    recipe.Recipe.save_recipe(data)
    return redirect('/dashboard')

@app.route('/recipes/edit/<int:id>', methods=['POST'])
def edit_recipes():
    if 'user_id' not in session:
        return redirect('/')

    data = {
        "recipes.id": request.form['id'],
        "name": request.form['name'],
        "descriptions": request.form['descriptions'],
        "instruction": request.form['instructions'],
        "date": request.form['date'],
        "under_30": request.form['under_30'],
        "updated_at": request.form['updated_at']
    }

    recipe.update_recipe(data)
    return redirect('/dashboard')

@app.route('/route/<int:id>')
def show_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('show_recipe.html', this_recipe=recipe.Recipe.get_one_recipe())