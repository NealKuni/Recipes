from flask_app import app
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL


class Recipe:
    db = "recipes_schema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under_30 = data['under_30']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.user = None

    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes;"
        
        recipes_table = connectToMySQL(cls.db).query_db(query)
        recipes = []

        for each_row in recipes_table:
            recipes.append(cls(each_row))
        return recipes

    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date, under_30, user_id) VALUES (%(name)s,%(description)s,%(instructions)s,%(date)s,%(under_30)s, %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def create_recipe(cls,data):
        query = "INSERT INTO recipes (name, description, instruction, date, duration) VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_30)s);"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def update_recipe(cls,data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instructions)s, date = %(date)s, duration = %(under_30)s WHERE recipes.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def destroy_recipe(cls,data):
        query = "DELETE * FROM recipes WHERE recipes.id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_one_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(id)s;"
        one_recipe = connectToMySQL(cls.db).query_db(query,data)
        return cls(one_recipe[0])
