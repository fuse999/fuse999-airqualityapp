"""Minimal flask app"""

from flask import Flask
import requests
import flask_sqlalchemy

#Make the application
app = Flask(__name__)

#make the route
@app.route("/")

#now we define a function
def root():
    return 'TODO - part 2 and beyond!'