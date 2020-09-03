# -*-coding:utf-8-*
import os

class Deliveroo():
	def __init__(self):
		self.URLlogin="https://restaurant-hub.deliveroo.net"

class JustEat():
	def __init__(self):
		self.URLlogin="https://partner.just-eat.fr/login"

class Oracle():
	def __init__(self):
		self.URLlogin="https://euf04-ohra-prod.hospitality.oracleindustry.com/login.jsp"
class Uber():
	def __init__(self):
		self.URLlogin="https://auth.uber.com/login/"
		self.RedirectURL="https://restaurant.uber.com/home/6adb16db-fd58-4d22-a972-5016b0ff8c53?state=vRc9lg-7KtGvGqbJ6-PDuVrVM2vhtxRF2J77saf1_oM%3D&_csid=qIO5t86C3ahMnUrwIgQQAg#_"


#chemin vers chromedriver.exe => '/home/<user>/chrome/chromedriver.exe'
#Pour que les scripts fonctionnent il faut installer chromedriver
if os.name=='nt':
	path='C:\\Users\\coren\\Documents\\chromedriver\\chromedriver.exe'
	pdfpath='C:\\Users\\coren\\Documents\\'
	command='python C:\\Users\\coren\\Documents\\infos\\otacos\\env\\Scripts\\pdf2txt.py'
	htmlpath='C:\\Users\\coren\\Documents\\infos\\otacos\\php\\pythonScript\\file.html'
else:
	path="/usr/bin/chromedriver"
	pdfpath='/tmp/mypdf/'
	command='python3 /usr/local/bin/pdf2txt.py'
	htmlpath='/tmp/mypdf/file.html'

#le fichier qui contient les infos pour se connecter
#On le crée s'il n'existe pas (/etc/mysql/conf.d/mysql.cnf)
#de la forme suivante:
#[client]
#user=<nom_user>
#password=<pass>
#host=<host>
#database=<db_name>
option_file="/etc/mysql/conf.d/mysql.cnf"

Deliveroo = Deliveroo()
JustEat=JustEat()
Oracle=Oracle()
Uber=Uber()
