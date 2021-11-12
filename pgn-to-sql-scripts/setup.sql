/*!rating table creation*/;

DROP TABLE IF EXISTS `ratings`;

CREATE TABLE `ratings` (
  `rating_name` varchar(22) NOT NULL,
  PRIMARY KEY (`rating_name`),
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;


/*!ratings table creation*/;

DROP TABLE IF EXISTS `players`;

CREATE TABLE `players` (
  `player_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `rating_name` varchar(22) DEFAULT NOT NULL,
  `favorite_opening` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`player_id`),
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;


/*!openings table creation*/;

DROP TABLE IF EXISTS `openings`;

CREATE TABLE `openings` (
  `opening_id` int(11) NOT NULL AUTO_INCREMENT,
  `opening_name` varchar(255) NOT NULL,
  PRIMARY KEY (`opening_id`),
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;



/*!game table creation*/;

DROP TABLE IF EXISTS `games`;

CREATE TABLE `games` (
  `games_id` int(11) NOT NULL AUTO_INCREMENT,
  `white_player` varchar(255) DEFAULT NOT NULL,
  `black_player` varchar(255) DEFAULT NULL,
  'result' varchar(11) Default NOT NULL,
  'opening_id' int(11) Default NOT NULL,
  PRIMARY KEY (`game_id`),
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
