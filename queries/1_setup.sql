

DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings (
  rating_name varchar(22) NOT NULL,
  PRIMARY KEY (rating_name)); 


DROP TABLE IF EXISTS players;
CREATE TABLE players (
  player_id varchar(17) NOT NULL,
  rating_name varchar(22)  NOT NULL,
  favorite_opening varchar(255)  NULL,
  PRIMARY KEY (player_id));



DROP TABLE IF EXISTS openings;
CREATE TABLE openings (
  opening_id varchar(11) NOT NULL,
  opening_name varchar(255) NOT NULL,
  PRIMARY KEY (opening_id));


DROP TABLE IF EXISTS games;
CREATE TABLE games (
  game_id int(11) NOT NULL AUTO_INCREMENT,
  white_player varchar(255)  NULL,
  black_player varchar(255)  NULL,
  result varchar(11)  NOT NULL,
  opening_id varchar(11)  NOT NULL,
  PRIMARY KEY (game_id));
