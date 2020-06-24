# -*-coding:UTF-8-*
from anticaptchaofficial.recaptchav2proxyless import *
from selenium import webdriver
import json
import time
from configuration import Uber,path
from selenium.webdriver.common.action_chains import ActionChains
import time
from env.config import apiKey,websiteKey

"""Script pour récupérer les données du site de Uber"""

account=""
passphrase=""
pinCode=""

def main():
	try:
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
					# RestoRate=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[2]/a/div[2]').text
					# NbRestoRate=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[2]/a/div[3]').text.replace('&nbsp;','')

					# Income7lastDays=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]').text.replace('&nbsp;','').replace('\n','')
					# Income714LastDays=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]').text.replace('&nbsp;','').replace('\n','')
					# AverageOrderPrice=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[3]').text.replace('\n','')

					# driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/div[2]').click()
					# time.sleep(1)

					# Orders7lastDays=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]').text.replace('\n','')
					# Orders714LastDays=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]').text.replace('\n','')

					# MissOrders=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]').text.replace('\n','')
					# WrongOrders=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/div[2]').text.replace('\n','')
					# InactivityTime=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/div[2]').text.replace('\n','')


					# BestFood=driver.find_elements_by_css_selector('#root > div > div.af.ag.ae.ah > div.am.e0.b3.e1.e2.e3.e4.e5 > div.ai.e6 > div.am.b3.e3 > div:nth-child(1) > div:nth-child(1) > div.ed.am.b3 > div')
					# for elem in BestFood:
					# 	tab=[]
					# 	for e in elem.find_elements_by_tag_name('div'):
					# 		tab.append(e.text.replace("'"," "))
					# 	Stat1Object[i]=tab
					# 	i+=1

					# NameBestRate=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[1]/div[2]').text.replace('\n','').replace("'"," ")
					# PercentBestRate=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div[2]/div/div').text.replace('\n','')

					# NameLowerRate=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[3]/div[1]/div[2]').text.replace('\n','').replace("'"," ")
					# PercentLowerRate=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div/div').text.replace('\n','')


					# driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div[2]/ul/li[2]/a/div').click()
					# time.sleep(5)

					# PercentAverageMarkbycustomers=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[3]/div[1]/div[3]/div/div/div/div[1]').text.replace('\n','')
					# PercentAverageMarkbydeliveryMan=driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[3]/div[3]/div[2]/div[3]/div/div/div/div[1]').text.replace('\n','')

					# StatsObject={'RestaurantRate':RestoRate,
					# 			'NbRestaurantRate':NbRestoRate,
					# 			'IncomeLast7Days':Income7lastDays,
					# 			'Orders7lastDays':Orders7lastDays,
					# 			'IncomeLast714Days':Income714LastDays,
					# 			'Orders714LastDays':Orders714LastDays,
					# 			'last7DaysAverageOrderPrice':AverageOrderPrice,
					# 			'last7DaysMissOrders':MissOrders,
					# 			'last7DaysWrongOrders':WrongOrders,
					# 			'last7DaysInactivityTime':InactivityTime,
					# 			'BestFood':Stat1Object,
					# 			'NameBestFood':NameBestRate,
					# 			'PercentBestRate':PercentBestRate,
					# 			'NameLowerFood':NameLowerRate,
					# 			'PercentLowerRate':PercentLowerRate,
					# 			'PercentAverageMarkbycustomers':PercentAverageMarkbycustomers,
					# 			'PercentAverageMarkbydeliveryMan':PercentAverageMarkbydeliveryMan}
				driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/div[1]/ul/li[3]/a').click()
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
					PaymentDate=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[3]/div/div/div/div/div[1]/ul/li[4]/div').text.replace('\n','')

				except:
					TotalIncome=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[4]/div/div/div/div/div[1]/ul/li[1]/div').text.replace('\n','')
					Orders=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[4]/div/div/div/div/div[1]/ul/li[2]/div').text.replace('\n','')
					PaymentDate=driver.find_element_by_xpath('/html/body/div/div/main/div/div[2]/div[4]/div/div/div/div/div[1]/ul/li[4]/div').text.replace('\n','')
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
				FullObjectJSON=json.dumps(FullObject,ensure_ascii=False)
				return FullObjectJSON
	except NoSuchElementException as exception:
		return "Impossible de récupérer les données, les identifiants sont peut être incorrects (UBER) id :"+account+" pass :"+passphrase+", il faut peut être utiliser anti captcha!"

if __name__=='__main__':
	#account='diengmoussa802+3@gmail.com'
	#passphrase='6adb16db1'
	#pinCode='5468'
	account="otacos.montreuilumiere@resto-tacos.fr"
	passphrase="Agoratech931"
	pinCode="9310"
	print(main())

