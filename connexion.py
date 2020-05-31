import mysql.connector
from configuration import option_file

try:
	mydb = mysql.connector.connect(
		#si vous n'utilisez pas option_files (qui consiste à regrouper
		#dans un fichier les informations de connexion) alors il faut faire:
		user='corentin',
		password='h8795642klm',
		database='otacos',
		host='localhost'
	     # option_files=option_file
	)
	cursor = mydb.cursor()
	print('connected to database')
except:
	print('unable to connect the database')
