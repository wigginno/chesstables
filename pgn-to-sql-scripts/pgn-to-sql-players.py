# Copyright (c) 2017, balping
# https://github.com/balping

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pgn
import sys
import hashlib

fields = ['player_id', 'rating_name', 'favorite_opening']

def elo_to_rating_name(elo):
	cutoffs = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]
	ratings = ['Class J', 'Class I', 'Class H', 'Class G', 'Class F', 'Class E',\
				 'Class D', 'Class C', 'Class B', 'Class A', 'Expert',\
				 'National Master', 'Senior Master']

	for i in range(13):
		if i == 12 or elo < cutoffs[i]:
			break
	
	return ratings[i]

def values_row (game):
	white_val = '    (\''
	black_val = '    (\''

	if hasattr(game, "white"):
		white_val += getattr(game, "white")
	else:
		return None

	if hasattr(game, "whiteelo"):
		white_val += '\', (SELECT rating_name from ratings WHERE rating_name=\''
		whiteElo = int(getattr(game, "whiteelo"))
		white_val += elo_to_rating_name(whiteElo) + '\')'
	else:
		return None
	
	if hasattr(game, "black"):
		black_val += getattr(game, "black")
	else:
		return None
	
	if hasattr(game, "blackElo"):
		black_val += '\', (SELECT rating_name from ratings WHERE rating_name=\''
		blackElo = int(getattr(game, "blackelo"))
		black_val += elo_to_rating_name(blackElo) + '\')'
	else:
		return None
	
	if hasattr(game, "eco"):
		white_val += ', (SELECT opening_id FROM openings WHERE opening_id=\''
		white_val += getattr(game, "eco") + '\')),\n'
		black_val += ', (SELECT opening_id FROM openings WHERE opening_id=\''
		black_val += getattr(game, "eco") + '\'))'
	else:
		return None

	vals = white_val + black_val
	
	return vals


if len(sys.argv) != 2:
	print('Usage: python pgn-to-sql-players.py input.pgn > out.sql')


i = 0
trailing_char = ''
for game in pgn.GameIterator(sys.argv[1]):

	val_row = values_row(game)
	if not val_row:
		break

	print(trailing_char)

	if (i % 500) == 0:
		print('INSERT INTO players (' + ', '.join(fields) + ') VALUES')
		print ('ON DUPLICATE KEY UPDATE')

	print(val_row, end='')

	if (i % 500) == 499:
		trailing_char = ';\n'
	else:
		trailing_char = ','

	i += 1


print(';', end='')
