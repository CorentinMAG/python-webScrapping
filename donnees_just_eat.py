# -*-coding:utf-8-*
from selenium import webdriver
import json
import time
from configuration import JustEat,path

"""Script pour scrapper les données du site Just Eat"""

#les valeurs de ces variables sont en base et sont remplies automatiquement par le script script_cron.py
account=""
passphrase=""

def main():
	try:

		#init
		FullObject=dict()
		ArticlesObject=dict()
		StatsObject=dict()
		MethodObject=dict()
		InvoiceObject=dict()
		FullStatsObject=dict()
		i=0

		#run chrome with headless option
		options=webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument('lang=fr')
		options.add_argument('log-level=3')
		driver = webdriver.Chrome(options=options,executable_path=path)
		driver.get(JustEat.URLlogin)

		assert "Just Eat" in driver.title

		#log-in
		login=driver.find_element_by_name('login')
		# login.send_keys(JustEat.login_data['login'])
		login.send_keys(account)
		password=driver.find_element_by_name('password')
		# password.send_keys(JustEat.login_data['password'])
		password.send_keys(passphrase)
		driver.find_element_by_class_name('button').click()
		time.sleep(1)

		#daily order
		articles = driver.find_elements_by_tag_name('section')
		if articles !=[]:
			for article in articles:
				priceElement = article.find_element_by_class_name('total').find_element_by_tag_name('strong')
				price = priceElement.text
				HourElement = article.find_element_by_tag_name('ul').find_element_by_class_name('delivery-time').find_element_by_tag_name('strong')
				hour = HourElement.text
				AddressElement=article.find_element_by_class_name('customer-address')
				address=AddressElement.text
				NameElement=article.find_element_by_class_name('customer').find_element_by_tag_name('span')
				Name=NameElement.text
				Numero=article.find_element_by_class_name('id').text
				ArticlesObject[i]={'price':price,'hour':hour,'address':address,'name':Name,'Numero':Numero}
				i+=1
			total = driver.find_element_by_class_name('orders-info').find_elements_by_tag_name('strong')[1].text
			ArticlesObject['total']=total
		else:
			ArticlesObject['data']='pas de données ce jour-ci'



		js="""let anchor = document.querySelector('.analytics');
		anchor.click();"""
		driver.execute_script(js)

		time.sleep(3)

		#stats of the month
		StatTitle = driver.find_element_by_class_name('pie').find_element_by_tag_name('h1')
		Title = StatTitle.text
		StatsObject['title']=Title
		payements = driver.find_element_by_class_name('card').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
		for payement in payements:
			method_name=payement.find_elements_by_tag_name('td')[0].text
			commandes=payement.find_elements_by_tag_name('td')[1].text
			totalperpayement=payement.find_elements_by_tag_name('td')[2].text
			MethodObject[method_name]={'commandes':commandes,'price':totalperpayement}
		total = driver.find_element_by_tag_name('tfoot').find_elements_by_tag_name('td')[2].text
		totalCommandes = driver.find_element_by_tag_name('tfoot').find_elements_by_tag_name('td')[1].text
		StatsObject['methods']=MethodObject
		StatsObject['total']=total
		StatsObject['totalCommandes']=totalCommandes
		FullStatsObject['Valide']=StatsObject
		StatsObject=dict()
		MethodObject=dict()

		js="""let anchor=document.querySelector('#app > div > main > div > article > div > section.table.summary > div > div > p:nth-child(2) > a');
		anchor.click();"""
		driver.execute_script(js)


		time.sleep(3)

		StatTitle = driver.find_element_by_class_name('pie').find_element_by_tag_name('h1')
		Title = StatTitle.text
		StatsObject['title']=Title
		payements = driver.find_element_by_class_name('card').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
		for payement in payements:
			method_name=payement.find_elements_by_tag_name('td')[0].text
			commandes=payement.find_elements_by_tag_name('td')[1].text
			totalperpayement=payement.find_elements_by_tag_name('td')[2].text
			MethodObject[method_name]={'commandes':commandes,'price':totalperpayement}
		total = driver.find_element_by_tag_name('tfoot').find_elements_by_tag_name('td')[2].text
		totalCommandes = driver.find_element_by_tag_name('tfoot').find_elements_by_tag_name('td')[1].text
		StatsObject['methods']=MethodObject
		StatsObject['total']=total
		StatsObject['totalCommandes']=totalCommandes
		FullStatsObject['Annule']=StatsObject


		js="""let anchor = document.querySelector('.invoices');
		anchor.click();"""
		driver.execute_script(js)

		time.sleep(3)

		#invoice of the month
		totalttc = driver.find_element_by_class_name('total').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[1].find_element_by_tag_name('strong').text
		InvoiceDate = driver.find_elements_by_class_name('info')[1].find_element_by_tag_name('ul').find_elements_by_tag_name('li')[1].find_element_by_tag_name('strong').text
		try:
			solde = driver.find_element_by_class_name('page-break').find_element_by_tag_name('table').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[2].find_elements_by_tag_name('td')[3].find_element_by_tag_name('strong').text
		except:
			solde=driver.find_element_by_class_name('page-break').find_element_by_tag_name('table').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[3].find_elements_by_tag_name('td')[3].find_element_by_tag_name('strong').text
		totalHT=driver.find_element_by_class_name('total').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[0].find_elements_by_tag_name('td')[1].find_element_by_tag_name('strong').text
		TVA=driver.find_element_by_class_name('total').find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')[1].find_elements_by_tag_name('td')[1].find_element_by_tag_name('strong').text
		NumFacture=driver.find_element_by_css_selector('div.info:nth-child(3) > ul:nth-child(2) > li:nth-child(3) > strong:nth-child(2)').text
		FactureCode=driver.find_element_by_css_selector('div.info:nth-child(3) > ul:nth-child(2) > li:nth-child(1) > strong:nth-child(2)').text
		RestaurantCode=driver.find_element_by_css_selector('div.info:nth-child(3) > ul:nth-child(2) > li:nth-child(5) > strong:nth-child(2)').text
		CompteComptable=driver.find_element_by_css_selector('div.info:nth-child(3) > ul:nth-child(2) > li:nth-child(4) > strong:nth-child(2)').text
		TvaKey=driver.find_element_by_css_selector('.total > div:nth-child(2) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > strong:nth-child(1)').text
		Ventes10TVA=driver.find_element_by_xpath('//*[@id="app"]/div/main/div/article/div/section[1]/div[2]/div/table/tbody/tr[2]/td[3]').text
		CollectedTVA = driver.find_element_by_xpath('//*[@id="app"]/div/main/div/article/div/section[1]/div[2]/div/table/tbody/tr[2]/td[3]').text.replace('€','').replace(',','.').replace(' ','')
		InvoiceObject[TvaKey]=TVA
		InvoiceObject['totalHT']=totalHT
		InvoiceObject['totalTTC']=totalttc
		InvoiceObject['Ventes HT 10% TVA']=Ventes10TVA
		InvoiceObject['TVA collecté']=round(float(CollectedTVA)*0.1,3)
		InvoiceObject['invoiceDate']=InvoiceDate
		InvoiceObject['solde']=solde
		InvoiceObject['NumFacture']=NumFacture
		InvoiceObject['codeFacture']=FactureCode
		InvoiceObject['coderestaurant']=RestaurantCode

		driver.quit()


		FullObject['DailyOrder']=ArticlesObject
		FullObject['MonthlyStats']=FullStatsObject
		FullObject['invoice']=InvoiceObject

		FullObjectJSON = json.dumps(FullObject,ensure_ascii=False)
		return FullObjectJSON
	########################################################
	except:
		return "impossible de récupérer les données, les identifiants sont peut-être incorrects"


if __name__=='__main__':
	account='25673otacos'
	passphrase='boursin'
	print(main())


