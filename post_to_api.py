import requests 

def post_data_to_api(content,dossier):
	print(dossier)
	url="https://saas.irf-cloud.com/irfservice/services/irfservice.svc/company/{"+dossier+"}/entries"
	headers ={
		'Content-Type': 'application/xml',
    	'IRF-Token':'STXiHqhhgB6sFyOA1E6p9cGs2cvf39Muf11BZiIviU/T58AO/3oiuWx0XwYmcuIfMk4DzS9YG4/zhd3g47adniR3G7hmvsSEVhFdaO/xthTBDIe0CqnOWRAV6ylKccNY/y+cq/t82CfgXsLFVsW8uyu3Lr54XaXRFz/O4zobhiscIKf0npZeEQONgiZJwdXOgxYxa2/q+4z5oTAEnXSXIBVcAp6wL2WTtRIpD+YzkOJkfKGN6lLOPLjevVbH5Nez47UCjoBbD54RdYoL0ukELFvhPB+5XvZdOyf23X0E6SWwmaebO3giKfurQYZKXGXb4+22SayfFx3IqGNtlBwrbhO07VKV7Ne+hA/wtkhBZbHWneyZkHb2tMd4gtZSC8aDc/TJ2EIxY8gXeGFnPncNRsfufOwpiiu+UufNKzUzEOPVV3A9NHPe7G+EcCw5H4lA+j+sWJUg1EHqvqZ3UNeEJRIIr+XzcyKbil2up0IhAZ2EBS+MQmWQZwfp2gBSZX2j',
    	'IRF-partnerID':'5A932DAF-820E-4E71-A3B6-700CA9E511C5'
	}
	z = requests.post(url, data = content.encode('utf-8'), headers = headers)
	print(z.text)



