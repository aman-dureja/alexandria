# Import flask and template operators
from flask import Flask, render_template

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import a module / component using its blueprint handler variable (mod_auth)
# from app.FOO.controllers import mod_FOO as FOO_module

# Register blueprint(s)
# app.register_blueprint(FOO_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
