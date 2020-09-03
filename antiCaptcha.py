# -*-coding:UTF-8-*
from anticaptchaofficial.recaptchav2proxyless import *
from selenium import webdriver
import json
import time
from configuration import Uber,path
from selenium.webdriver.common.action_chains import ActionChains
import time
from env.config import apiKey,websiteKey,UBER
from post_to_api import post_data_to_api

"""Script pour récupérer les données du site de Uber"""

account=""
passphrase=""
pinCode=""
dossier=""

def main():
	#try:
	FullObject=dict()
	Stat1Object=dict()
	i=0

	solver = recaptchaV2Proxyless()
	solver.set_verbose(1)
	solver.set_key(apiKey)
	solver.set_website_url("https://auth.uber.com/login/")
	solver.set_website_key(websiteKey)

	#run chrome with headless option
	options=webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('lang=fr')
	options.add_argument('log-level=3')
	driver = webdriver.Chrome(options=options,executable_path=path)
	driver.get(Uber.URLlogin)
	time.sleep(5)
	#log-in
	mail=driver.find_element_by_id('useridInput')
	mail.send_keys(account)
	driver.find_element_by_tag_name('button').click()
	time.sleep(5)
	try:
		g_response = solver.solve_and_return_solution()

		if g_response != 0:
			time.sleep(4)
			driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % g_response)
			time.sleep(2)
			driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/form/button').click()
			time.sleep(2)
		else:
			print("task finished with error "+solver.error_code)
	finally:
		password = driver.find_element_by_id('password')
		password.send_keys(passphrase)
		driver.find_element_by_tag_name('button').click()
		time.sleep(5)
		if driver.title!="Restaurant Analytics":
			driver.get(Uber.RedirectURL)
			time.sleep(5)

			driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div[1]/ul/li[5]/a').click()
			time.sleep(5)

			pin=driver.find_element_by_id('pin-code')
			pin.send_keys(pinCode)

			driver.find_element_by_xpath('/html/body/div/div/div/div/form/button').click()
			time.sleep(10)

			try:
				TotalIncome=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[3]/div/div/div/div/div[1]/ul/li[1]/div').text.replace('\n','')
			except:
				driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[1]/div/span/ul/li[6]/a').click()
				time.sleep(2)
				driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[1]/div/span/ul/li[5]/a').click()
				time.sleep(4)

			try:
				DateRange=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[2]/div[1]/div/div/div/div/input').get_attribute('value')
			except:
				DateRange=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[3]/div[1]/div/div/div/div/input').get_attribute('value')
			
			try:
				TotalIncome=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[3]/div/div/div/div/div[1]/ul/li[1]/div').text.replace('\n','')
				Orders=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[3]/div/div/div/div/div[1]/ul/li[2]/div').text.replace('\n','')
				a=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[3]/div/div/div/div/div[1]/ul/li[4]/div').text.replace('\n','')
				b=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[3]/div/div/div/div/div[1]/ul/li[4]/div/span').text.replace('\n','')
				PaymentDate=a.replace(b,'')
				PaymentDate=datetime.strptime(PaymentDate,'%a %b %d %Y').strftime('%Y-%m-%d')

			except:
				TotalIncome=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[4]/div/div/div/div/div[1]/ul/li[1]/div').text.replace('\n','')
				Orders=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[4]/div/div/div/div/div[1]/ul/li[2]/div').text.replace('\n','')
				a=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[4]/div/div/div/div/div[1]/ul/li[4]/div').text.replace('\n','')
				b=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[4]/div/div/div/div/div[1]/ul/li[4]/div/span').text.replace('\n','')
				PaymentDate=a.replace(b,'')
				PaymentDate=datetime.strptime(PaymentDate,'%a %b %d %Y').strftime('%Y-%m-%d')
			Frais={}
			Versement={}

			try:
				tableauBody=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[3]/div/div/div/div/div[2]/table/tbody')
				
			except:
				tableauBody=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[4]/div/div/div/div/div[2]/table/tbody')
			trs=tableauBody.find_elements_by_tag_name('tr')

			Revenu=trs[0].find_elements_by_tag_name('td')[2].text
			AllFrais=trs[1].find_elements_by_tag_name('td')[2].text

			trs[1].find_element_by_tag_name('i').click()
			time.sleep(2)
			trNewFrais=tableauBody.find_elements_by_class_name('bg-uber-white-10')
			for tr in trNewFrais:
				if 'TVA comprise' in tr.text or 'including VAT' in tr.text:
					Frais['frais Uber']=tr.find_elements_by_tag_name('td')[2].text
				if 'Bonus' in tr.text or 'prime' in tr.text:
					Frais['Bonus']=tr.find_elements_by_tag_name('td')[2].text
				if 'Ajustements' in tr.text or 'adjustement' in tr.text:
					Frais['ajustement']=tr.find_elements_by_tag_name('td')[2].text
				if 'Misc' in tr.text:
					Frais['Misc Payment']=tr.find_elements_by_tag_name('td')[2].text
			trs[1].find_element_by_tag_name('i').click()

			TotalVersement=trs[2].find_elements_by_tag_name('td')[2].text
			trs[2].find_element_by_tag_name('i').click()
			time.sleep(2)
			trNewVersement=tableauBody.find_elements_by_class_name('bg-uber-white-10')
			for tr in trNewVersement:
				if 'bancaire' in tr.text or 'bank' in tr.text:
					Versement['VersementBancaire']=tr.find_elements_by_tag_name('td')[2].text
				if 'Tickets Restaurant' in tr.text or 'Voucher' in tr.text:
					Versement['Ticket Resto']=tr.find_elements_by_tag_name('td')[2].text
		

			driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[1]/div/span/ul/li[4]/a').click()
			time.sleep(3)

			AllOrders={}
			j=0
			for order in driver.find_elements_by_class_name('_style_2T0IvR'):
				line=[]
				for element in order.find_elements_by_tag_name('td'):
					line.append(element.text)
				AllOrders[j]=line
				j+=1
			
			Frais['AllFrais']=AllFrais

			Versement['Total Versement']=TotalVersement
			

			IncomeObject={
				'DateRange':DateRange,
				'PaymentDate':PaymentDate,
				'Revenu':Revenu,
				'Frais':Frais,
				'TotalVersement':Versement,
				'AllOrders':AllOrders
			}


			FullObject={
				'payment':IncomeObject
			}
			driver.quit()
			bonus=round(float(Frais['frais Uber'].replace('(','').replace(')','').replace('€','').replace(',','.').replace(' ',''))/1.2,2)
			com=round(bonus*0.2,2)
			cb=Versement['VersementBancaire'].replace('€','').replace(',','.').replace(' ','')
			try:
				Versement['Ticket Resto']
				tkresto=Versement['Ticket Resto'].replace('€','').replace(',','.').replace(' ','')
			except:
				tkresto = 0
			sldt=round((float(Revenu.replace('€','').replace(',','.').replace(' ',''))/1.1),2)
			tvacoll=round((sldt*0.1),2)
			date_td=datetime.today().strftime('%Y-%m-%d')
			data="""<importEntryRequest>\n
			<importDate>"""+date_td+"""</importDate>\n
			<wsImportEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + PaymentDate + """</date>\n
			<accountNumber>6222000000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>""" + str(bonus) + """</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + PaymentDate + """</date>\n
			<accountNumber>4456600000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>""" + str(com) + """</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + PaymentDate + """</date>\n
			<accountNumber>5112000000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>""" + str(cb) + """</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + PaymentDate + """</date>\n
			<accountNumber>5114000000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>""" + str(tkresto) + """</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + PaymentDate + """</date>\n
			<accountNumber>7070000000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>""" + str(sldt) + """</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + PaymentDate + """</date>\n
			<accountNumber>4457100000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>""" + str(tvacoll) + """</debit>\n
			</importEntry>\n
			</wsImportEntry>\n
			</importEntryRequest>\n
			""" 

			post_data(data,dossier)

			FullObjectJSON=json.dumps(FullObject,ensure_ascii=False)
			return FullObjectJSON
	#except NoSuchElementException as exception:
	#	return "Impossible de récupérer les données, les identifiants sont peut être incorrects (UBER) id :"+account+" pass :"+passphrase+", il faut peut être utiliser anti captcha!"

def post_data(data,dossier):
	print(data)
	post_data_to_api(data,dossier)

if __name__=='__main__':
	account=UBER['account']
	passphrase=UBER['password']
	pinCode=UBER['pin']
	dossier=UBER['dossier']
	print(main())

