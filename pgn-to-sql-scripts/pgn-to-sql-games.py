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

fields = ['white', 'black', 'eco', 'result']

def values_row (game):
	vals = '    ('

	for field in fields:
		if hasattr(game, field):
			val = getattr(game, field)
			if field in ['white', 'black']:
				val = '(SELECT playerID from players WHERE playerID=\'' + val + '\')'
				vals += val + ', '
			else:
				vals += '\'' + val.replace('\'', '\\\'') + '\', '
		else:
			return None

	vals = vals.rstrip(', ')
	vals += ')'
	
	return vals


if len(sys.argv) != 2:
	print('Usage: python pgn-to-sql-games.py input.pgn > out.sql')


i = 0
trailing_char = ''
for game in pgn.GameIterator(sys.argv[1]):

	val_row = values_row(game)
	if not val_row:
		break

	print(trailing_char)

	if (i % 500) == 0:
		print('INSERT INTO games (' + ', '.join(fields) + ') VALUES')

	print(val_row, end='')

	if (i % 500) == 499:
		trailing_char = ';\n'
	else:
		trailing_char = ','

	i += 1


print(';', end='')
