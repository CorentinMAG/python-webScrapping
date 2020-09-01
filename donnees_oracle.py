# -*-coding:utf-8-*
from selenium import webdriver
import json
import time
from configuration import Oracle,path
from post_to_api import post_data_to_api
from datetime import datetime



"""Script pour scrapper les données du site Oracle"""

account=""
companyphrase=""
passphrase=""
dossier=""

def main():
	#try:

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

	try:
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
	except:
		pass

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

	try:
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
	except:
		pass

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

	try:

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

	except:
		pass
	driver.quit()

	vht10tva=float(FullObject['TaxB'][1][4].replace('€','').replace(',','.').replace(' ',''))+float(FullObject['TaxB'][2][4].replace('€','').replace(',','.').replace(' ',''))
	vcol10=float(FullObject['TaxB'][1][2].replace('€','').replace(',','.').replace(' ',''))+float(FullObject['TaxB'][2][2].replace('€','').replace(',','.').replace(' ',''))
	vht5tva=float(FullObject['TaxB'][3][4].replace('€','').replace(',','.').replace(' ',''))+float(FullObject['TaxB'][4][4].replace('€','').replace(',','.').replace(' ',''))
	vcol5=float(FullObject['TaxB'][3][2].replace('€','').replace(',','.').replace(' ',''))+float(FullObject['TaxB'][4][2].replace('€','').replace(',','.').replace(' ',''))
	especeR=FullObject['ReglementB'][2][1].replace(',','.').replace(' ','')
	cbR=FullObject['ReglementB'][1][1].replace(',','.').replace(' ','')
	tkrR=FullObject['ReglementB'][3][1].replace(',','.').replace(' ','')
	tab_date=FullObject['TaxTitle'][1][2].split(" ")
	if tab_date[0] == "JAN":
		tab_date[0] = "01"
	elif tab_date[0] == "FEB":
		tab_date[0] = "02"
	elif tab_date[0] == "MAR":
		tab_date[0] = "03"
	elif tab_date[0] == "APR":
		tab_date[0] = "04"
	elif tab_date[0] == "MAY":
		tab_date[0] = "05"
	elif tab_date[0] == "JUN":
		tab_date[0] = "06"
	elif tab_date[0] == "JUL":
		tab_date[0] = "07"
	elif tab_date[0] == "AUG":
		tab_date[0] = "08"
	elif tab_date[0] == "SEP":
		tab_date[0] = "09"
	elif tab_date[0] == "OCT":
		tab_date[0] = "10"
	elif tab_date[0] == "NOV":
		tab_date[0] = "11"
	elif tab_date[0] == "DEC":
		tab_date[0] = "12"
	date=tab_date[2]+"-"+tab_date[0]+"-"+tab_date[1]
	date_td=datetime.today().strftime('%Y-%m-%d')
	data="""<importEntryRequest>
				<importDate>"""+str(date_td)+"""</importDate>
				<wsImportEntry>
					<importEntry>
						<journalRef>VT</journalRef>
						<date>""" +str(date)+ """</date>
						<accountNumber>7071000000</accountNumber>
						<description>Ventes HT 10% TVA</description>
						<credit>""" + str(vht10tva) + """</credit>
						<debit>0</debit>
					</importEntry>
					<importEntry>
						<journalRef>VT</journalRef>
						<date>""" + str(date) + """</date>
						<accountNumber>4457100000</accountNumber>
						<description>TVA collectees 10%</description>
						<credit>""" + str(vcol10) + """</credit>
						<debit>0</debit>
					</importEntry>
					<importEntry>
						<journalRef>VT</journalRef>
						<date>""" + str(date) + """</date>
						<accountNumber>7075000000</accountNumber>
						<description>Ventes HT 5% TVA</description>
						<credit>""" + str(vht5tva) + """</credit>
						<debit>0</debit>
					</importEntry>
					<importEntry>
						<journalRef>VT</journalRef>
						<date>""" + str(date) + """</date>
						<accountNumber>4457100000</accountNumber>
						<description>TVA collectees 5%</description>
						<credit>""" + str(vcol5) + """</credit>
						<debit>0</debit>
					</importEntry>
					<importEntry>
						<journalRef>VT</journalRef>
						<date>""" + str(date) + """</date>
						<accountNumber>5110000000</accountNumber>
						<description>Especes</description>
						<credit>0</credit>
						<debit>"""+ str(especeR) + """</debit>
					</importEntry>
					<importEntry>
						<journalRef>VT</journalRef>
						<date>""" + str(date) + """</date>
						<accountNumber>5800000000</accountNumber>
						<description>Carte bancaire</description>
						<credit>0</credit>
						<debit>""" + str(cbR) + """</debit>
					</importEntry>
					<importEntry>
						<journalRef>VT</journalRef>
						<date>""" + str(date) + """</date>
						<accountNumber>5111000000</accountNumber>
						<description>Ticket restaurant</description>
						<credit>0</credit>
						<debit>""" + str(tkrR) + """</debit>
					</importEntry>
					<importEntry>
						<journalRef>VT</journalRef>
						<date>""" + str(date) + """</date>
						<accountNumber>5800000000</accountNumber>
						<description>Ecart</description>
						<credit>""" + str(round(vht10tva+vcol10+vht5tva+vcol5+float(especeR)+float(cbR)+float(tkrR),2)) + """</credit>
						<debit>0</debit>
					</importEntry>
					</wsImportEntry>
			</importEntryRequest>"""

	post_data(data,dossier)

	FullObjectJSON = json.dumps(FullObject,ensure_ascii=False)
	return FullObjectJSON
	#except:
	#	return "Impossible de récupérer les données, les identifiants sont peut-être incorrects"


def post_data(data,dossier):
	print(data)
	post_data_to_api(data,dossier)


if __name__=='__main__':
	print(main())

