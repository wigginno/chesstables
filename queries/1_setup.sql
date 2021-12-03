DROP TABLE IF EXISTS games;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS openings;
DROP TABLE IF EXISTS ratings;

CREATE TABLE ratings (
  rating_name varchar(22) NOT NULL PRIMARY KEY
);

CREATE TABLE openings (
  opening_id varchar(11) NOT NULL PRIMARY KEY,
  opening_name varchar(255) NOT NULL
);

CREATE TABLE players (
  player_id varchar(17) NOT NULL PRIMARY KEY,
  rating_name varchar(22)  NOT NULL,
  favorite_opening varchar(255)  NULL,
  CONSTRAINT fk_rating_name
    FOREIGN KEY(rating_name)
    REFERENCES ratings (rating_name)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_favorite_opening
    FOREIGN KEY(favorite_opening)
    REFERENCES openings (opening_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE games (
  game_id int(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
  white_player varchar(255)  NULL,
  black_player varchar(255)  NULL,
  result varchar(11)  NOT NULL,
  opening_id varchar(11)  NOT NULL,
  CONSTRAINT fk_white_player
    FOREIGN KEY(white_player)
    REFERENCES players (player_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_black_player
    FOREIGN KEY(black_player)
    REFERENCES players (player_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_opening_id
    FOREIGN KEY(opening_id)
    REFERENCES openings (opening_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);
