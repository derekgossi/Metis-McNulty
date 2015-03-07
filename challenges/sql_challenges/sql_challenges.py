import MySQLdb

# Connect to MySQL DB
db = MySQLdb.connect(host='localhost', user='root', passwd='', db='tennis')

# Get the DB cursor
cursor = db.cursor()

# Define our tables for the analysis
tables = ['aus_ladies_2013', 'aus_men_2013', 'french_ladies_2013', 'french_men_2013', 
			'us_ladies_2013', 'us_men_2013', 'wimbledon_ladies_2013', 'wimbledon_men_2013']

# CHALLENGE # 1


for table in tables:
	raw_input("Press Enter to continue...")

	query  = 'SELECT player, sum(player_count) AS num_matches FROM \
			((SELECT player1 AS player, count(player1) AS player_count FROM ' + str(table) + ' GROUP BY player1) UNION \
			(SELECT player2 AS player, count(player2) AS player_count FROM ' + str(table) + ' GROUP BY player2)) t \
			GROUP BY player;'
	
	cursor.execute(query)
	for row in cursor.fetchall():
		print row




