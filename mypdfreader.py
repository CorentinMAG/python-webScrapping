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

	montant_total = driver.find_element_by_xpath("/html/body/div[20]/span").text.replace(".","").replace(",",".")
	commission = driver.find_element_by_xpath("/html/body/div[24]/span").text.replace(",",".")
	frais_supplementaire = driver.find_element_by_xpath("/html/body/div[42]/span").text.replace(",",".")

	# try:
	# 	if 'Nouvelle' or 'New' in driver.find_element_by_xpath("/html/body/div[17]/span"):
	# 		montant_total = driver.find_element_by_xpath("/html/body/div[24]/span").text.replace(".","").replace(",",".")
	# 		commission = driver.find_element_by_xpath("/html/body/div[39]/span").text.replace(",",".")
	# 		frais_supplementaire = driver.find_element_by_xpath("/html/body/div[54]/span").text.replace(",",".")
	# 	else:
	# 		montant_total = driver.find_element_by_xpath("/html/body/div[21]/span").text.replace(".","").replace(",",".")
	# 		commission = driver.find_element_by_xpath("/html/body/div[31]/span").text.replace(",",".")
	# 		frais_supplementaire = driver.find_element_by_xpath("/html/body/div[46]/span").text.replace(",",".")
	# except:
	# 	montant_total = driver.find_element_by_xpath("/html/body/div[21]/span").text.replace(".","").replace(",",".")
	# 	commission = driver.find_element_by_xpath("/html/body/div[31]/span").text.replace(",",".")
	# 	frais_supplementaire = driver.find_element_by_xpath("/html/body/div[46]/span").text.replace(",",".")
	# finally:
	montant_total = float(montant_total)
	commission = float(commission)
	frais_supplementaire = float(frais_supplementaire)
	total_debit = commission + frais_supplementaire
	montant_total_a_payer = round(montant_total - (commission + frais_supplementaire),2)

	thead = ["Montant total de la commande TTC","Commission","Frais Supplémentaires","total Débit","Montant total à payer"]
	tbody = [montant_total,commission,frais_supplementaire,total_debit,montant_total_a_payer]


	time.sleep(2)
	driver.quit()
	os.remove(htmlpath)

	obj={
		'Thead':thead,
		'Tbody':tbody
	}
	return obj
if __name__=='__main__':
	print(main())







