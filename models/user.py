from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
import re
from flask import render_template, redirect, request, session, flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)


class User:
    db = "recipes_schema"

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipe = []

    @classmethod
    def save_user(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s,%(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)
    

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        if len(results) == 0:
            return redirect('/')
        return cls(results[0])

    @staticmethod 
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) == 0:
            flash('First name is required.')
            is_valid = False
        if len(user['last_name']) == 0:
            flash('Last name is required.')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(user['password']) <8:
            flash('password must be at least 8 characters long')
        if user['password'] != user['confirm_password']:
            is_valid = False
            flash("Passwords don't match.")

    @staticmethod 
    def validate_login(data):
        is_valid = True
        if len(data['email']) == 0:
            is_valid = False
            flash('An email is required.', 'error')
        if len(data['password']) == 0:
            is_valid = False
            flash('A password is required.', 'error')
        return is_valid