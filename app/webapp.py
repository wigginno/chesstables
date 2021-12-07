from flask import Flask, render_template
from flask import request, redirect
from db_connector import connect_to_database, execute_query
webapp = Flask(__name__)

webapp.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# TODO - fix issue on update player:
#   Cannot delete or update a parent row: a foreign key constraint fails
#       (`chesstables`.`games`, CONSTRAINT `fk_black_player` FOREIGN KEY
#       (`black_player`) REFERENCES `players` (`player_id`))')

@webapp.route('/')
def index():
    return render_template('index.html')

@webapp.route('/games')
def Games():
    db_connection = connect_to_database()
    next_game_id_query = "SELECT AUTO_INCREMENT FROM information_schema.tables\
         WHERE table_schema = \"cs340_wigginno\" and table_name = \"games\";"
    
    next_game_id = execute_query(db_connection, next_game_id_query).fetchall()
    last_game_id = next_game_id[0][0] - 1
    
    last_page = last_game_id // 500 + 1
    page_number = int(request.args.get('page', 1))

    min_id = 500*(page_number - 1) + 1
    max_id = min_id + 499

    get_games_query = "SELECT * FROM games WHERE game_id>=%d AND game_id<=%d;"\
         % (min_id, max_id)
    games = execute_query(db_connection, get_games_query).fetchall()
    openings = get_openings(db_connection)

    return render_template('Games.html', openings=openings, games=games,\
         page_number=page_number, last_page=last_page)

@webapp.route('/openings')
def Openings():
    db_connection = connect_to_database()
    get_openings_query = "SELECT opening_id, opening_name FROM openings;"
    openings = execute_query(db_connection, get_openings_query).fetchall()
    
    return render_template('Openings.html', openings=openings)

@webapp.route('/players')
def Players():
    db_connection = connect_to_database()
    get_players_query = "SELECT * FROM players;"
    players = execute_query(db_connection, get_players_query).fetchall()
    openings = get_openings(db_connection)

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
    add_rating_query = "INSERT INTO ratings (rating_name) VALUES (\'%s\');"\
         % (rating_name)
    try:
        execute_query(db_connection, add_rating_query)
    except:
        pass
    return redirect('/ratings')

@webapp.route('/addopening', methods=['POST'])
def addopening():
    db_connection = connect_to_database()
    opening_id=request.form['opening_id']
    opening_name=request.form['opening_name']
    add_opening_query = '''INSERT INTO openings (opening_id, opening_name) 
        VALUES (\'%s\', \'%s\');''' % (opening_id, opening_name)
    try:
        execute_query(db_connection, add_opening_query)
    except:
        pass
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
    
    try:
        execute_query(db_connection, add_opening_query)
    except:
        pass

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
    
    try:
        execute_query(db_connection, add_game_query)
    except:
        pass

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

@webapp.route('/deleterating')
def deleterating():
    rating_name = request.args.get('rating_name')
    
    if rating_name:
        db_connection = connect_to_database()
        del_rating_query = "DELETE FROM ratings WHERE rating_name='%s';"\
             % rating_name
        try:
            execute_query(db_connection, del_rating_query)
        except:
            pass

    return redirect('/ratings')

@webapp.route('/deleteopening')
def deleteopening():
    opening_id = request.args.get('opening_id')
    
    if opening_id:
        db_connection = connect_to_database()
        del_opening_query = "DELETE FROM openings WHERE opening_id='%s';"\
             % opening_id
        try:
            execute_query(db_connection, del_opening_query)
        except:
            pass

    return redirect('/openings')
    

@webapp.route('/deleteplayer')
def deleteplayer():
    player_id = request.args.get('player_id')

    if player_id:
        db_connection = connect_to_database()
        del_player_query = "DELETE FROM players WHERE player_id='%s';"\
             % player_id
        try:
            execute_query(db_connection, del_player_query)
        except:
            pass

    return redirect('/players')

@webapp.route('/deletegame')
def deletegame():
    game_id = request.args.get('game_id')

    if game_id:
        db_connection = connect_to_database()
        del_game_query = "DELETE FROM games WHERE game_id=%s;" % (game_id)
        try:
            execute_query(db_connection, del_game_query)
        except:
            pass

    return redirect('/games')

@webapp.route('/updaterating', methods=['POST'])
def updaterating():
    rating_name = request.form.get('id')
    new_rating_name = request.form.get('rating_name')
    
    if new_rating_name:
        db_connection = connect_to_database()
        update_rating_name_query = "UPDATE ratings SET rating_name='%s'\
         WHERE rating_name='%s';" % (new_rating_name, rating_name)
        try:
            execute_query(db_connection, update_rating_name_query)
        except:
            pass

    return redirect('/ratings')

@webapp.route('/updateopening', methods=['POST'])
def updateopening():
    opening_id = request.form.get('id')
    new_opening_id = request.form.get('opening_id')
    opening_name = request.form.get('opening_name')

    if new_opening_id:
        db_connection = connect_to_database()
        update_opening_id_query = "UPDATE openings SET opening_id='%s'\
         WHERE opening_id='%s';" % (new_opening_id, opening_id)
        try:
            execute_query(db_connection, update_opening_id_query)
        except:
            pass
        opening_id = new_opening_id

    if opening_name:
        db_connection = connect_to_database()
        update_opening_name_query = "UPDATE openings SET opening_name='%s'\
         WHERE opening_id='%s';" % (opening_name, opening_id)
        try:
            execute_query(db_connection, update_opening_name_query)
        except:
            pass

    return redirect('/openings')

@webapp.route('/updateplayer', methods=['POST'])
def updateplayer():
    player_id = request.form['id']
    new_player_id = request.form.get('player_id')
    rating_name = request.form.get('rating_name')
    favorite_opening = request.form.get('favorite_opening')

    if new_player_id:
        db_connection = connect_to_database()
        update_player_id_query = "UPDATE players SET player_id='%s'\
             WHERE player_id='%s';" % (new_player_id, player_id)
        try:
            execute_query(db_connection, update_player_id_query)
        except:
            pass
        player_id = new_player_id

    if rating_name:
        db_connection = connect_to_database()
        update_rating_name_query = "UPDATE players SET rating_name='%s'\
             WHERE player_id='%s';" % (rating_name, player_id)
        try:
            execute_query(db_connection, update_rating_name_query)
        except:
            pass

    if favorite_opening:
        db_connection = connect_to_database()
        update_fav_opening_query = "UPDATE players SET favorite_opening='%s'\
             WHERE player_id='%s';" % (favorite_opening, player_id)
        try:
            execute_query(db_connection, update_fav_opening_query)
        except:
            pass

    return redirect('/players')

@webapp.route('/updategame', methods=['POST'])
def updategame():
    game_id = request.form.get('game_id')
    white_player = request.form.get('white_player')
    black_player = request.form.get('black_player')
    result = request.form.get('result')
    opening_id = request.form.get('opening_id')
    
    if white_player:
        db_connection = connect_to_database()
        update_white_player_id_query = "UPDATE games SET white_player='%s'\
             WHERE game_id='%s';" % (white_player, game_id)
        try:
            execute_query(db_connection, update_white_player_id_query)
        except:
            pass

    if black_player:
        db_connection = connect_to_database()
        update_black_player_id_query = "UPDATE games SET black_player='%s'\
             WHERE game_id='%s';" % (black_player, game_id)
        try:
            execute_query(db_connection, update_black_player_id_query)
        except:
            pass

    if result:
        db_connection = connect_to_database()
        update_result_query = "UPDATE games SET result='%s'\
             WHERE game_id='%s';" % (result, game_id)
        try:
            execute_query(db_connection, update_result_query)
        except:
            pass

    if opening_id:
        db_connection = connect_to_database()
        update_opening_id_query = "UPDATE games SET opening_id='%s'\
             WHERE game_id='%s';" % (opening_id, game_id)
        try:
            execute_query(db_connection, update_opening_id_query)
        except:
            pass

    return redirect('/games')

@webapp.route('/updateplayerform')
def updateplayerform():
    db_connection = connect_to_database()
    id = request.args.get('player_id')
    attributes = ['player_id', 'rating_name', 'favorite_opening']
    entity_name = 'player'
    openings = get_openings(db_connection)
    return render_template('updateform.html', id=id, attributes=attributes,\
         entity_name=entity_name, openings=openings)

@webapp.route('/updategameform')
def updategameform():
    db_connection = connect_to_database()
    id = request.args.get('game_id')
    attributes = ['game_id', 'white_player', 'black_player',\
         'result', 'opening_id']
    entity_name = 'game'
    openings = get_openings(db_connection)
    return render_template('updateform.html', id=id, attributes=attributes,\
         entity_name=entity_name, openings=openings)

@webapp.route('/updateopeningform')
def updateopeningform():
    id = request.args.get('opening_id')
    attributes = ['opening_id', 'opening_name']
    entity_name = 'opening'
    return render_template('updateform.html', id=id, attributes=attributes,\
         entity_name=entity_name)

@webapp.route('/updateratingform')
def updateratingform():
    id = request.args.get('rating_name')
    attributes = ['rating_name']
    entity_name = 'rating'
    return render_template('updateform.html', id=id, attributes=attributes,\
         entity_name=entity_name)
    
def get_openings(db_connection):
    get_openings_query = "SELECT opening_id FROM openings;"
    openings = execute_query(db_connection, get_openings_query).fetchall()
    return openings

# update form variables:
#   entity_name
#   id
#   attributes
