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

"""Script pour récupérer les données du site de Uber

"""

account=""
passphrase=""
pinCode=""
dossier=""

def main():
	try:

		# captcha solver
		solver = recaptchaV2Proxyless()
		solver.set_verbose(1)
		solver.set_key(apiKey)
		solver.set_website_url("https://auth.uber.com/login/")
		solver.set_website_key(websiteKey)

		#run chrome with headless option
		options=webdriver.ChromeOptions()
		#options.add_argument('headless')
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
		# if we can acess directly the password field we don't need to run the captcha bypass
		try:
			driver.find_element_by_id('password')
		except:
			g_response = solver.solve_and_return_solution()

			if g_response != 0:
				time.sleep(4)
				driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML = "%s"' % g_response)
				time.sleep(2)
				driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/form/div[2]/button').click()
				time.sleep(2)
			else:
				print("task finished with error "+solver.error_code)

		password = driver.find_element_by_id('password')
		password.send_keys(passphrase)
		driver.find_element_by_tag_name('button').click()
		time.sleep(5)
		if driver.title!="Restaurant Analytics":
			driver.get(Uber.RedirectURL)
			time.sleep(5)

			# pour aller sur le payment screen (Paiements)
			try:
				driver.find_element_by_link_text('Payments').click()
			except:
				driver.find_element_by_link_text('Paiements').click()
			time.sleep(5)

			# input pour entrer le code pin
			pin=driver.find_element_by_id('pin-code')
			pin.send_keys(pinCode)

			driver.find_element_by_tag_name('button').click()
			time.sleep(10)


			# squelette de la facture
			ul = driver.find_elements_by_tag_name('ul')
			if len(ul) <= 3:
				driver.refresh()
				time.sleep(5)
			ul = driver.find_elements_by_tag_name('ul')[2]


			# invoice elements
			lis = ul.find_elements_by_tag_name('li')

			# initialise dictionary which is going to handle all the latest invoice
			invoice = {}
			input = driver.find_element_by_tag_name('input')
			invoice['periode'] = input.get_attribute('value')

			# we don't care of the latest element
			for li in lis[:-1]:
				label = li.find_element_by_tag_name('span').text.strip()

				# sometimes, value element contains child we don't want. To handle this, we get 
				# all the text and we remove the useless part.
				val_el = li.find_element_by_tag_name('div')
				all_value = val_el.text.replace('€','').replace('\n','').strip()
				child = val_el.find_elements_by_xpath('./child::*')
				if len(child) !=0:
					ch_value = child[0].text.strip()
					value = all_value.replace(ch_value,'').replace('\n','')
				else:
					value = all_value
				invoice[label] = value

			# detail of the invoice
			detail = {}

			# table containing all the details
			table = driver.find_element_by_tag_name('table')
			tbody = table.find_element_by_tag_name('tbody')
			trs = tbody.find_elements_by_tag_name('tr')
			for tr in trs:
				tds = tr.find_elements_by_tag_name('td')

				# expand the tr
				tds[0].find_element_by_tag_name('i').click()

				lab_el = tds[1]
				all_label = lab_el.text.strip()

				child = lab_el.find_elements_by_xpath("./child::*")
				if len(child) != 0:
					ch_value = child[0].text.strip()
					label = all_label.replace(ch_value,'')
				else:
					label = all_label

				# menu deroulant
				sub = tbody.find_elements_by_class_name('bg-uber-white-10')
				if len(sub) != 0:
					sub_detail = {}
					for s in sub:
						sub_td = s.find_elements_by_tag_name('td')
						sub_label = sub_td[1].text.replace('\n','').strip()
						sub_value = sub_td[2].text.replace('\n','').replace('€','').replace('(','').replace(')','').strip()
						sub_detail[sub_label] = sub_value

				# cacher le menu déroulant
				tds[0].find_element_by_tag_name('i').click()

				value = tds[2].text.replace('(','').replace(')','').replace('€','').strip()
				detail[label] = {'total':value,'sub':sub_detail}

			invoice['detail'] = detail

			driver.quit()
			date_td=datetime.today().strftime('%Y-%m-%d')

			## date
			try:
				d = invoice['Payment Date']
			except:
				d = invoice['Date du paiement']
			payment_date = datetime.strptime(d,'%a %b %d %Y').strftime('%Y-%m-%d')

			## uber com
			try:
				com = invoice['detail']['Frais et autres paiements']['sub']['Frais Uber (TVA comprise)']
			except:
				try:
					com = invoice['detail']['Fees and other payments']['sub']['Uber Fee (including VAT)']
				except:
					pass

			## cb
			try:
				cb = invoice['detail']['Versement total']['sub']['Votre versement bancaire']
			except:
				try:
					cb = invoice['detail']['Total Payout']['sub']['Your bank payout']
				except:
					pass

			#ticket resto
			try:
				tkresto = invoice['detail']['Versement total']['sub']['Revenus en Tickets Restaurant® Edenred']
			except:
				try:
					tkresto = invoice['detail']['Total Payout']['sub']['Voucher earnings']
				except:
					pass

			# earnings
			try:
				revenu = invoice['detail']['Revenus']['total']
			except:
				try:
					revenu = invoice['detail']['Earnings']['total']
				except:
					pass


			#bonus ?

			# compensation
			try:
				compensation = invoice['detail']['Fees and other payments']['Ajustements liés à des erreurs de commande (TVA comprise)']
			except:
				try:
					compensation = invoice['detail']['Fees and other payments']['Order Error Adjustments (including VAT)']
				except:
					pass


			data="""<importEntryRequest>\n
			<importDate>"""+date_td+"""</importDate>\n
			<wsImportEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + payment_date + """</date>\n
			<accountNumber>6222000000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>0</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + payment_date + """</date>\n
			<accountNumber>4456600000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>""" + com + """</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + payment_date + """</date>\n
			<accountNumber>5112000000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>""" + cb + """</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + payment_date + """</date>\n
			<accountNumber>5114000000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>""" + tkresto + """</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + payment_date + """</date>\n
			<accountNumber>7070000000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>""" + revenu + """</credit>\n
			<debit>0</debit>\n
			</importEntry>\n
			<importEntry>\n
			<journalRef>VT</journalRef>\n
			<date>""" + payment_date + """</date>\n
			<accountNumber>4457100000</accountNumber>\n
			<description>VENTE UBER EATS</description>\n
			<credit>0</credit>\n
			<debit>0</debit>\n
			</importEntry>\n
			</wsImportEntry>\n
			</importEntryRequest>\n
			""" 

			post_data(data,dossier)

			FullObjectJSON = json.dumps(invoice,ensure_ascii=False)
			return FullObjectJSON
	except NoSuchElementException as exception:
		return "Impossible de récupérer les données, les identifiants sont peut être incorrects (UBER) id :"+account+" pass :"+passphrase+", il faut peut être utiliser anti captcha!"

def post_data(data,dossier):
	print(data)
	post_data_to_api(data,dossier)

if __name__=='__main__':
	account=UBER['account']
	passphrase=UBER['password']
	pinCode=UBER['pin']
	dossier=UBER['dossier']
	print(main())


