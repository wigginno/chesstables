from flask import Flask, render_template
from flask import request, redirect
from db_connector import connect_to_database, execute_query
webapp = Flask(__name__)

@webapp.route('/')
def index():
    return render_template('index.html')

@webapp.route('/Games')
def Games():
    return render_template('Games.html')

@webapp.route('/Openings')
def Openings():
    return render_template('Openings.html')

@webapp.route('/Players')
def Players():
    return render_template('Players.html')

@webapp.route('/Ratings')
def Ratings():
    return render_template('Ratings.html')
