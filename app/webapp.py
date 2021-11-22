from flask import Flask, render_template
from flask import request, redirect
from db_connector import connect_to_database, execute_query
webapp = Flask(__name__)

@webapp.route('/')
def index():
    return render_template('index.html')

@webapp.route('/games')
def Games():
    db_connection = connect_to_database()
    next_game_id_query = "SELECT AUTO_INCREMENT FROM information_schema.tables\
         WHERE table_schema = \"chesstables\" and table_name = \"games\";"
    
    next_game_id = execute_query(db_connection, next_game_id_query).fetchall()
    last_game_id = next_game_id[0][0] - 1
    
    last_page = last_game_id // 500 + 1
    page_number = int(request.args.get('page', 1))

    min_id = 500*(page_number - 1) + 1
    max_id = min_id + 499

    get_games_query = "SELECT * FROM games WHERE game_id>=%d AND game_id<=%d;"\
         % (min_id, max_id)
    games = execute_query(db_connection, get_games_query).fetchall()
    
    get_openings_query = "SELECT opening_id FROM openings;"
    openings = execute_query(db_connection, get_openings_query).fetchall()
    openings_list = []
    
    for o in openings:
        id=str(o)[2:5]
        openings_list.append(id)
    
    openings = openings_list

    return render_template('Games.html', openings=openings, games=games,\
         page_number=page_number, last_page=last_page)

@webapp.route('/openings')
def Openings():
    db_connection = connect_to_database()
    get_openings_query = "SELECT * FROM openings;"
    openings = execute_query(db_connection, get_openings_query).fetchall()
    
    return render_template('Openings.html', openings=openings)

@webapp.route('/players')
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

@webapp.route('/ratings')
def Ratings():
    db_connection = connect_to_database()
    get_ratings_query = "SELECT * FROM ratings;"
    ratings = execute_query(db_connection, get_ratings_query).fetchall()
    return render_template('Ratings.html', ratings=ratings)

@webapp.route('/addrating', methods=['POST'])
def addrating():
    db_connection = connect_to_database()
    rating_name = request.form['rating_name']
    add_rating_query = "INSERT INTO ratings (rating_name) VALUES (%s);"\
         % (rating_name)
    execute_query(db_connection, add_rating_query)
    return redirect('/ratings')

@webapp.route('/addopening', methods=['POST'])
def addopening():
    db_connection = connect_to_database()
    opening_id=request.form['opening_id']
    opening_name=request.form['opening_name']
    add_opening_query = '''INSERT INTO openings (opening_id, opening_name) 
        VALUES (\'%s\', \'%s\');''' % (opening_id, opening_name)
    execute_query(db_connection, add_opening_query)
    return redirect('/openings')

@webapp.route('/addplayer', methods=['POST'])
def addplayer():
    db_connection = connect_to_database()
    player_id=request.form['player_id']
    rating_name=request.form['rating_name']
    favorite_opening = request.form['favorite_opening']
    add_opening_query = '''INSERT INTO players (player_id, rating_name, 
        favorite_opening) VALUES (\'%s\', \'%s\', \'%s\');''' %\
             (player_id, rating_name, favorite_opening)
    execute_query(db_connection, add_opening_query)
    return redirect('/players')

@webapp.route('/addgame', methods=['POST'])
def addgame():
    db_connection = connect_to_database()
    white_player=request.form['white_player']
    black_player=request.form['black_player']
    result=request.form['result']
    opening_id=request.form['opening_id']
    add_game_query = '''INSERT INTO games (white_player, black_player, result, 
        opening_id) VALUES (\'%s\', \'%s\', \'%s\', \'%s\')''' %\
         (white_player, black_player, result, opening_id)
    execute_query(db_connection, add_game_query)
    return redirect('/games')

@webapp.route('/filtergames')
def filtergames():
    # filter games by opening and/or player_id
    opening_id = request.args.get('opening_id')
    player_id = request.args.get('player_id')
    
    if not opening_id and not player_id:
        return redirect('/games')
    
    db_connection = connect_to_database()
    filter_games_query = "SELECT * FROM games WHERE "

    if opening_id and player_id:
        filter_games_query += ("opening_id=\'%s\' AND (white_player=\'%s\'\
             OR black_player=\'%s\');" % (opening_id, player_id, player_id))
    elif opening_id: # filter by only opening_id
        filter_games_query += ("opening_id=\'%s\';" % (opening_id))
    else: # filter by only player_id
        filter_games_query += ("white_player=\'%s\' OR black_player=\'%s\';"\
             % (player_id, player_id))

    games = execute_query(db_connection, filter_games_query).fetchall()

    return render_template('filtergames.html', games=games)# TODO: Make filtergames page

@webapp.route('/filterplayers')
def filterplayers():
    # filter players by favorite_opening and/or player_id
    favorite_opening = request.args.get('favorite_opening')
    player_id = request.args.get('player_id')
    
    if not favorite_opening and not player_id:
        return redirect('/players')
    
    db_connection = connect_to_database()
    filter_players_query = "SELECT * FROM players WHERE "

    if favorite_opening and player_id:
        filter_players_query += ("favorite_opening=\'%s\' AND player_id=\'%s\';" %\
         (favorite_opening, player_id))
    elif favorite_opening: # filter by only opening_id
        filter_players_query += ("favorite_opening=\'%s\';" % (favorite_opening))
    else: # filter by only player_id
        filter_players_query += ("player_id=\'%s\';" % (player_id))

    players = execute_query(db_connection, filter_players_query).fetchall()

    return render_template('filterplayers.html', players=players)
