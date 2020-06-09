# -*-coding:utf-8-*
from selenium import webdriver
import json
import time
from configuration import Oracle,path



"""Script pour scrapper les données du site Oracle"""

account=""
companyphrase=""
passphrase=""

def main():
	try:

		#init
		FullObject=dict()

		#run chrome with headless option
		options=webdriver.ChromeOptions()
		options.add_argument('headless')
		options.add_argument('lang=fr')
		options.add_argument('log-level=3')
		driver = webdriver.Chrome(options=options,executable_path=path)
		driver.get(Oracle.URLlogin)

		#log-in
		user=driver.find_element_by_id('usr')
		user.send_keys(account)
		company=driver.find_element_by_id('cpny')
		company.send_keys(companyphrase)
		password=driver.find_element_by_id('pwd')
		password.send_keys(passphrase)
		driver.find_element_by_id('Login').click()

		assert "Reporting" in driver.title

		sideMenu = driver.find_element_by_id('sideMenu')
		driver.switch_to.frame(sideMenu)
		time.sleep(10)
		DailyReport = driver.find_element_by_link_text('Rapport Jour').click()
		time.sleep(15)

		driver.switch_to.default_content()

		TableFrame = driver.find_element_by_id('myPage')
		driver.switch_to.frame(TableFrame)
		ReportsFrame = driver.find_element_by_id('reportsFrame')
		driver.switch_to.frame(ReportsFrame)
		time.sleep(10)

		totalCAHT = driver.find_elements_by_css_selector('td.col_header_1')[1].text
		FullObject['total_CA_HT']=totalCAHT

		tab=driver.find_element_by_css_selector('body > div:nth-child(6)').find_element_by_tag_name('table')

		thead=tab.find_elements_by_css_selector('thead tr td')
		objThead=list()
		for t in thead:
			if t.text =='Moyenne Temps SOS':
				pass
			else:
				objThead.append(t.text)
		FullObject['thead']=objThead

		tbody=tab.find_elements_by_css_selector('tbody tr')
		v=0
		for e in tbody:
			listeobj=list()
			for r in e.find_elements_by_tag_name('td'):
				if r.text=="":
					pass
				else:
					listeobj.append(r.text)
			FullObject[v]=listeobj
			v+=1

		driver.switch_to.default_content()
		driver.switch_to.frame(sideMenu)
		driver.find_element_by_link_text('More Reports...').click()
		time.sleep(10)
		driver.switch_to.default_content()
		TableFrameReport = driver.find_element_by_id('myPage')
		driver.switch_to.frame(TableFrameReport)
		js="""
		let tr = document.querySelectorAll("tr[class='h2_block']")[4];
		let tr1 =tr.nextElementSibling;
		tr1.querySelector('a').click();
		"""
		driver.execute_script(js)
		time.sleep(10)
		driver.switch_to.default_content()
		driver.switch_to.frame(TableFrameReport)
		reportsFrameTab=driver.find_element_by_id('reportsFrame')
		driver.switch_to.frame(reportsFrameTab)

		DivExploitTitle=driver.find_element_by_css_selector('body > div:nth-child(4)')
		DivExploitTab=driver.find_element_by_css_selector('body > div:nth-child(5) > table:nth-child(1)')
		tbody=DivExploitTab.find_elements_by_css_selector('tbody tr')
		y=0
		Exploitdic=dict()
		for u in tbody:
			listeobj=list()
			for r in u.find_elements_by_tag_name('td'):
				listeobj.append(r.text)
			Exploitdic[y]=listeobj
			FullObject['TaxTitle']=Exploitdic
			y+=1

		driver.switch_to.default_content()
		driver.switch_to.frame(sideMenu)
		time.sleep(10)
		driver.find_element_by_link_text('Rapport Des Taxes').click()
		time.sleep(15)
		driver.switch_to.default_content()
		TableFrame = driver.find_element_by_id('myPage')
		driver.switch_to.frame(TableFrame)
		reportsFrameTab=driver.find_element_by_id('reportsFrame')
		driver.switch_to.frame(reportsFrameTab)

		TableTax=driver.find_element_by_css_selector('body > div:nth-child(5) > table:nth-child(1)')
		thead=TableTax.find_elements_by_css_selector('thead tr td')
		objThead=list()
		for t in thead:
			objThead.append(t.text)
		FullObject['TaxT']=objThead

		tbody=TableTax.find_elements_by_css_selector('tbody tr')
		z=0
		RegleTax=dict()
		for e in tbody:
			listeobj=list()
			for r in e.find_elements_by_tag_name('td'):
				listeobj.append(r.text)
			RegleTax[z]=listeobj
			FullObject['TaxB']=RegleTax
			z+=1

		driver.switch_to.default_content()
		driver.switch_to.frame(sideMenu)
		time.sleep(10)
		driver.find_element_by_link_text('Rapport Mode Reglement').click()
		time.sleep(15)
		driver.switch_to.default_content()
		TableFrame = driver.find_element_by_id('myPage')
		driver.switch_to.frame(TableFrame)
		reportsFrameTab=driver.find_element_by_id('reportsFrame')
		driver.switch_to.frame(reportsFrameTab)

		tableReglement = driver.find_elements_by_tag_name('table')[1]
		thead=tableReglement.find_elements_by_css_selector('thead tr td')
		objThead=list()
		for t in thead:
			objThead.append(t.text)
		FullObject['ReglementT']=objThead

		tbody=tableReglement.find_elements_by_css_selector('tbody tr')
		v=0
		Regle=dict()
		for e in tbody:
			listeobj=list()
			for r in e.find_elements_by_tag_name('td'):
				listeobj.append(r.text)
			Regle[v]=listeobj
			FullObject['ReglementB']=Regle
			v+=1


		driver.quit()

		FullObjectJSON = json.dumps(FullObject,ensure_ascii=False)
		return FullObjectJSON
	except:
		return "Impossible de récupérer les données, les identifiants sont peut-être incorrects"

if __name__=='__main__':
	account='OTAPATAY'
	companyphrase='OTA'
	passphrase='Elena99$3'
	print(main())

