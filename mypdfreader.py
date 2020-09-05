from lxml import html
import codecs
import os
from selenium import webdriver
from configuration import Deliveroo,path,pdfpath,command,htmlpath
import time
import json


def main():
	if os.name!='nt':
		file = os.listdir(pdfpath)[0]
		pathpdffile=pdfpath+file
	else:
		file=os.listdir(pdfpath)[-2]
		pathpdffile=pdfpath+file
	os.system(("%s -o %s %s") % (command,htmlpath,pathpdffile))
	os.remove(pathpdffile)
	file = codecs.open(htmlpath, "r", "utf-8")
	file.close()
	options=webdriver.ChromeOptions()
	options.add_argument('lang=fr')
	options.add_argument('log-level=3')
	options.add_argument('headless')
		


	driver = webdriver.Chrome(options=options,executable_path=path)
	driver.get("file://%s" % (htmlpath));
	time.sleep(2)
	
	#la structure du pdf change souvent...
	all = driver.find_element_by_xpath('/html/body/div[61]/span[1]').text
	if 'Montant total de la commande TTC' in all:

		all = all.split('\n')

		thead = all[::2]
		tbody = all[1::2]
		
		suitethead=driver.find_element_by_xpath('/html/body/div[61]/span[2]').text
		suitetbody=driver.find_element_by_xpath('/html/body/div[61]/span[3]').text

		finalthead=driver.find_element_by_xpath('/html/body/div[61]/span[4]').text
		finaltbody=driver.find_element_by_xpath('/html/body/div[61]/span[5]').text
	else:
		all = driver.find_element_by_xpath('/html/body/div[60]/span[1]').text
		all = all.split('\n')

		thead=all[::2]
		tbody=all[1::2]

		suitethead=driver.find_element_by_xpath('/html/body/div[60]/span[2]').text
		suitetbody=driver.find_element_by_xpath('/html/body/div[60]/span[3]').text

		finalthead=driver.find_element_by_xpath('/html/body/div[60]/span[4]').text
		finaltbody=driver.find_element_by_xpath('/html/body/div[60]/span[5]').text


	thead.append(suitethead)
	thead.append(finalthead)

	tbody.append(suitetbody)
	tbody.append(finalthead)
	# try:
	# 	thead = driver.find_element_by_xpath('/html/body/div[57]/span').text.split("\n") # ok
	# 	if 'Montant total de la commande TTC' in thead[0]:
	# 		pass
	# 	else:
	# 		raise ValueError('Pas le bon, on passe au suivant')
	# except:
	# 	try:
	# 		thead = driver.find_element_by_xpath('/html/body/div[59]/span').text.split("\n") #ok
	# 		if 'Montant total de la commande TTC' in thead[0]:
	# 			pass
	# 		else:
	# 			raise ValueError('Pas le bon, on passe au suivant')
	# 	except:
	# 		try:
	# 			thead=driver.find_element_by_xpath('/html/body/div[58]/span').text.split("\n") #ok
	# 			if 'Montant total de la commande TTC' in thead[0]:
	# 				pass
	# 			else:
	# 				raise ValueError('Pas le bon, on passe au suivant')
	# 		except:
	# 			thead = driver.find_element_by_xpath('/html/body/div[60]/span').text.split("\n") #ok

	# for i,elem in enumerate(thead):
	# 	thead[i]=elem.replace("'"," ")
	# try:
	# 	tbody=driver.find_element_by_xpath('/html/body/div[58]/span[1]').text.split("\n")
	# 	if '€' in tbody[0]:
	# 		pass
	# 	else:
	# 		raise ValueError('Pas le bon, on passe au suivant')
	# except:
	# 	try:
	# 		tbody = driver.find_element_by_xpath('/html/body/div[60]/span[1]').text.split("\n")
	# 		if '€' in tbody[0]:
	# 			pass
	# 		else:
	# 			raise ValueError('Pas le bon, on passe au suivant')
	# 	except:
	# 		try:
	# 			tbody=driver.find_element_by_xpath('/html/body/div[59]/span[1]').text.split("\n")
	# 			if '€' in tbody[0]:
	# 				pass
	# 			else:
	# 				raise ValueError('Pas le bon, on passe au suivant')
	# 		except:
	# 			tbody =driver.find_element_by_xpath('/html/body/div[61]/span[1]').text.split("\n")
	# try:
	# 	suitethead = driver.find_element_by_xpath('/html/body/div[58]/span[2]').text.split("\n")
	# 	if 'Montant TTC facturable par Deliveroo' in suitethead[0]:
	# 		pass
	# 	else:
	# 		raise ValueError('Pas le bon, on passe au suivant')
	# except:
	# 	try:
	# 		suitethead=driver.find_element_by_xpath('/html/body/div[60]/span[2]').text.split("\n")
	# 		if 'Montant TTC facturable par Deliveroo' in suitethead[0]:
	# 			pass
	# 		else:
	# 			raise ValueError('Pas le bon, on passe au suivant')
	# 	except:
	# 		try:
	# 			suitethead=driver.find_element_by_xpath('/html/body/div[59]/span[2]').text.split("\n")
	# 			if 'Montant TTC facturable par Deliveroo' in suitethead[0]:
	# 				pass
	# 			else:
	# 				raise ValueError('Pas le bon, on passe au suivant')
	# 		except:
	# 			suitethead=driver.find_element_by_xpath('/html/body/div[61]/span[2]').text.split("\n")

	# for i,elem in enumerate(suitethead):
	# 	suitethead[i] = elem.replace("'"," ")
	# try:
	# 	suitetbody=driver.find_element_by_xpath('/html/body/div[58]/span[3]').text.split("\n")
	# 	if '€' in suitetbody[0]:
	# 		pass
	# 	else:
	# 		raise ValueError('Pas le bon, on passe au suivant')
	# except:
	# 	try:
	# 		suitetbody=driver.find_element_by_xpath('/html/body/div[60]/span[3]').text.split("\n")
	# 		if '€' in suitetbody[0]:
	# 			pass
	# 		else:
	# 			raise ValueError('Pas le bon, on passe au suivant')
	# 	except:
	# 		try:
	# 			suitetbody=driver.find_element_by_xpath('/html/body/div[59]/span[3]').text.split("\n")
	# 			if '€' in suitetbody[0]:
	# 				pass
	# 			else:
	# 				raise ValueError('Pas le bon, on passe au suivant')
	# 		except:
	# 			suitetbody=driver.find_element_by_xpath('/html/body/div[61]/span[3]').text.split("\n")

	time.sleep(2)
	driver.quit()
	os.remove(htmlpath)

	# FullThead=thead+suitethead
	# FullTbody=tbody+suitetbody

	obj={
		'Thead':thead,
		'Tbody':tbody
	}
	return obj
if __name__=='__main__':
	print(main())







