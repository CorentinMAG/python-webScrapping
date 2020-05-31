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
		file=os.listdir(pdfpath)[-1]
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
	try:
		thead = driver.find_element_by_xpath('/html/body/div[58]/span').text.split("\n")
	except:
		try:
			thead = driver.find_element_by_xpath('/html/body/div[58]/span').text.split("\n")
		except:
			thead=driver.find_element_by_xpath('/html/body/div[60]/span').text.split("\n")
	try:
		tbody=driver.find_element_by_xpath('/html/body/div[58]/span[1]').text.split("\n")
	except:
		try:
			tbody = driver.find_element_by_xpath('/html/body/div[59]/span[1]').text.split("\n")
		except:
			tbody=driver.find_element_by_xpath('/html/body/div[61]/span[1]').text.split("\n")
	try:
		suitethead = driver.find_element_by_xpath('/html/body/div[59]/span[2]').text.split("\n")
	except:
		try:
			suitethead=driver.find_element_by_xpath('/html/body/div[59]/span[2]').text.split("\n")
		except:
			suitethead=driver.find_element_by_xpath('/html/body/div[61]/span[2]').text.split("\n")
	try:
		suitetbody=driver.find_element_by_xpath('/html/body/div[59]/span[3]').text.split("\n")
	except:
		try:
			suitetbody=driver.find_element_by_xpath('/html/body/div[58]/span[3]').text.split("\n")
		except:
			suitetbody=driver.find_element_by_xpath('/html/body/div[61]/span[3]').text.split("\n")
	time.sleep(2)
	driver.quit()
	os.remove(htmlpath)

	FullThead=thead+suitethead
	FullTbody=tbody+suitetbody

	obj={
		'Thead':FullThead,
		'Tbody':FullTbody
	}
	return obj
if __name__=='__main__':
	print(main())







