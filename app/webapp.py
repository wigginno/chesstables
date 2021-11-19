from flask import Flask, render_template
from flask import request, redirect
from db_connector import connect_to_database, execute_query
webapp = Flask(__name__)

@webapp.route('/')
def index():
    return render_template('index.html')

@webapp.route('/Games')
def Games():
    db_connection = connect_to_database()
    
    get_games_query = "SELECT * FROM games;"
    games = execute_query(db_connection, get_games_query).fetchall()
    games = games[:100]
    
    get_openings_query = "SELECT opening_id FROM openings;"
    openings = execute_query(db_connection, get_openings_query).fetchall()
    openings_list = []
    
    for o in openings:
        id=str(o)[2:5]
        openings_list.append(id)
    
    openings = openings_list

    return render_template('Games.html', openings=openings, games=games)

@webapp.route('/Openings')
def Openings():
    db_connection = connect_to_database()
    
    get_openings_query = "SELECT * FROM openings;"
    openings = execute_query(db_connection, get_openings_query).fetchall()
    
    return render_template('Openings.html', openings=openings)

@webapp.route('/Players')
def Players():
    db_connection = connect_to_database()
    
    get_players_query = "SELECT * FROM players;"
    players = execute_query(db_connection, get_players_query).fetchall()

    get_openings_query = "SELECT opening_id FROM openings;"
    openings = execute_query(db_connection, get_openings_query).fetchall()
    openings_list = []
    
    for o in openings:
        id=str(o)[2:5]
        openings_list.append(id)
    
    openings = openings_list

    return render_template('Players.html', players=players, openings=openings)

@webapp.route('/Ratings')
def Ratings():
    db_connection = connect_to_database()
    
    get_ratings_query = "SELECT * FROM ratings;"
    ratings = execute_query(db_connection, get_ratings_query).fetchall()
    return render_template('Ratings.html', ratings=ratings)
