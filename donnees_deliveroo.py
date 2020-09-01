# -*-coding:UTF-8-*
from selenium import webdriver
import json
import time
import os
from configuration import Deliveroo,path
from configuration import pdfpath
import mypdfreader
import requests
from post_to_api import post_data_to_api

"""Script to retrieve data from deliveroo"""

account=""
passphrase=""
dossier=""

def main():
	#try:

			#init
	FullObject=dict()
	DailyOrders=dict()
	ReviewOfTheLast7Days=dict()
	InvoiceObject=dict()
	TodayOrder=dict()
	i=0
	j=0

	#run chrome with headless option
	options=webdriver.ChromeOptions()
	#options.add_argument("headless")
	options.add_argument('lang=fr')
	options.add_argument('log-level=3')
	#options.add_argument("--disable-dev-shm-usage") #fix problem on linux os
	#options.add_argument("--no-sandbox") #when run on docker 

	#options to enable pdf downloading
	options.add_experimental_option("prefs", {
		"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
 		 "download.default_directory": "%s" % (pdfpath) ,
  		"download.prompt_for_download": False,
  		"download.directory_upgrade": True,
  		"download.extensions_to_open": "applications/pdf",
  		"safebrowsing.enabled": True
		})
	

	driver = webdriver.Chrome(options=options,executable_path=path)
	driver.get(Deliveroo.URLlogin)
	enable_download_in_headless_chrome(driver,pdfpath)

	assert "Deliveroo" in driver.title

	#log-in
	email=driver.find_elements_by_tag_name('input')[0]
	email.send_keys(account)
	password=driver.find_elements_by_tag_name('input')[1]
	password.send_keys(passphrase)
	driver.find_element_by_tag_name('button').click()
	time.sleep(10)

	OrdersFinished = driver.find_elements_by_tag_name('h2')[0].text
	PreparationTime=driver.find_elements_by_tag_name('h2')[1].text
	TurnOver=driver.find_elements_by_tag_name('h2')[2].text
	CustomersMark = driver.find_elements_by_tag_name('h2')[5].text
	RefusedOrders=driver.find_elements_by_tag_name('h2')[3].text
	RefusedPercentage=driver.find_elements_by_tag_name('h2')[4].text
	ReviewOfTheLast7Days={"Commandes terminées":OrdersFinished,"Temps de préparation":PreparationTime,"Commandes refusées":RefusedOrders,"Pourcentage de refus":RefusedPercentage,"Chiffre affaire":TurnOver,"Note client":CustomersMark}

	js="""let anchor = document.querySelectorAll('a')[3];
	anchor.click();"""
	driver.execute_script(js)
	time.sleep(5)

	#daily order
	try:
		TotalOrders = driver.find_elements_by_tag_name('h2')[0].text
		OrdersConfirmed = driver.find_elements_by_tag_name('h2')[1].text
		DailyTurnOver = driver.find_elements_by_tag_name('h2')[2].text
		AllOrders=driver.find_elements_by_class_name('tcl__TableRow-188f4a81')
		for order in AllOrders:
			Number=order.find_elements_by_tag_name('div')[0].text
			Date=order.find_elements_by_tag_name('div')[1].text
			status=order.find_elements_by_tag_name('div')[2].text
			Price=order.find_elements_by_tag_name('div')[3].text
			TodayOrder[j]={'Commande':Number,'Date':Date,'status':status,'Price':Price}
			j+=1
		DailyOrders={"TotalOrders":TotalOrders,"ConfirmOrders":OrdersConfirmed,"DailyTurnOver":DailyTurnOver,"TodayOrder":TodayOrder}
	except:
		DailyOrders["data"]="Pas de commandes ce jour-ci"

	js="""let anchor = document.querySelectorAll('a')[6];
	anchor.click();"""
	driver.execute_script(js)

	#invoices
	time.sleep(10)
	test=driver.find_element_by_xpath('/html/body/div[1]/div[1]/main/div[2]/div/div[2]/div/div/div/div[2]/div[1]')
	a = test.find_element_by_tag_name('a')
	h=a.get_attribute('href')
	time.sleep(5)
	driver.get(h)
	time.sleep(5)

	pdfdetail=mypdfreader.main()

	time.sleep(3)
	try:
		Invoices = driver.find_elements_by_class_name('tcl__TableRow-188f4a81')
		for invoice in Invoices:
			num = invoice.find_elements_by_class_name('tcl__Text-03d692ab')[0].text
			date = invoice.find_elements_by_class_name('tcl__Text-03d692ab')[1].text
			price = invoice.find_elements_by_class_name('tcl__Text-03d692ab')[2].text
			InvoiceObject[i]={"acn":num,"date":date,"price":price}
			i+=1
	except:
		InvoiceObject['data']='Pas de factures'
	driver.quit()

	FullObject['ReviewOfTheLast7Days']=ReviewOfTheLast7Days
	FullObject['DailyOrders']=DailyOrders
	FullObject['Invoices']=InvoiceObject
	FullObject['PDFdetail']=pdfdetail

	date_td=datetime.today().strftime('%Y-%m-%d')
	data="""<importEntryRequest>\n
	<importDate>"""+str(date)+"""</importDate>\n
	<wsImportEntry>\n
	<importEntry>\n
	<journalRef>VT</journalRef>\n
	<date>""" + date_d + """</date>\n
	<accountNumber>7072000000</accountNumber>\n
	<description>DELIVEROO</description>\n
	<credit>""" + str(float(pdfdetail['Tbody'][0].replace('€','').replace(',','.').replace(' ',''))/1.1) + """</credit>\n
	<debit>0</debit>\n
	</importEntry>\n
	<importEntry>\n
	<journalRef>VT</journalRef>\n
	<date>""" + date_d + """</date>\n
	<accountNumber>5115000000</accountNumber>\n
	<description>DELIVEROO</description>\n
	<credit>0</credit>\n
	<debit>""" + pdfdetail['Tbody'][5].replace('€','').replace(',','.').replace(' ','') + """</debit>\n
	</importEntry>\n
	<importEntry>\n
	<journalRef>VT</journalRef>\n
	<date>""" + date_d + """</date>\n
	<accountNumber>6225000000</accountNumber>\n
	<description>DELIVEROO</description>\n
	<credit>0</credit>\n
	<debit>""" + str(float(pdfdetail['Tbody'][4].replace('€','').replace(',','.').replace(' ',''))/1.2) + """</debit>\n
	</importEntry>\n
	<importEntry>\n
	<journalRef>VT</journalRef>\n
	<date>""" + date_d + """</date>\n
	<accountNumber>4457100000</accountNumber>\n
	<description>DELIVEROO</description>\n
	<credit>""" + str((float(pdfdetail['Tbody'][0].replace('€','').replace(',','.').replace(' ',''))/1.1)*0.1) + """</credit>\n
	<debit>0</debit>\n
	/importEntry>\n
	<importEntry>\n
	<journalRef>VT</journalRef>\n
	<date>""" + date_d + """</date>\n
	<accountNumber>4456600000</accountNumber>\n
	<description>DELIVEROO</description>\n
	<credit>0</credit>\n
	<debit>"""+ str((float(pdfdetail['Tbody'][4].replace('€','').replace(',','.').replace(' ',''))/1.2)*0.2) + """</debit>\n
	</importEntry>\n
	</wsImportEntry>\n
	</importEntryRequest>\n
	"""

	post_data(data,dossier)

	FullObjectJSON = json.dumps(FullObject,ensure_ascii=False)
	return FullObjectJSON
	# except:
	# 	return "Impossible de récupérer les données, les identifiants sont peut-être incorrects"

def post_data(data,dossier):
	print(data)
	post_data_to_api(data,dossier)

def enable_download_in_headless_chrome(driver, download_dir):
	"""
	there is currently a "feature" in chrome where
	headless does not allow file download: https://bugs.chromium.org/p/chromium/issues/detail?id=696481
	This method is a hacky work-around until the official chromedriver support for this.
	Requires chrome version 62.0.3196.0 or above.
	"""

	# add missing support for chrome "send_command"  to selenium webdriver
	driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

	params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
	command_result = driver.execute("send_command", params)
	print("response from browser:")
	for key in command_result:
		print("result:" + key + ":" + str(command_result[key]))


if __name__=='__main__':
	print(main())

