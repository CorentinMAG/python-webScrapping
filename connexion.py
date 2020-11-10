import mysql.connector
from configuration import option_file
import os

try:
	if os.name=='nt':

		mydb = mysql.connector.connect(
			#si vous n'utilisez pas option_files (qui consiste à regrouper
			#dans un fichier les informations de connexion) alors il faut faire:
			user='corentin',
			password='vlgklm91',
			database='otacos',
			host='localhost',
			auth_plugin='mysql_native_password'
		     # option_files=option_file
		)
		cursor = mydb.cursor()
		print('connected to database')
	else:
		mydb = mysql.connector.connect(
			#si vous n'utilisez pas option_files (qui consiste à regrouper
			#dans un fichier les informations de connexion) alors il faut faire:
			user='user',
			password='',
			database='otacos',
			host='localhost'
		     # option_files=option_file
		)
		cursor = mydb.cursor()
		print('connected to database')
except:
	print('unable to connect the database')
