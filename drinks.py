import requests
from selenium import webdriver
from bs4 import BeautifulSoup


URL = "https://mixblendenjoy.com/limited-availability-products-whiskey/"
data = requests.get(URL)
soup = BeautifulSoup(data.text, "html.parser")

availableLiquors = {}
for cl in soup.find_all('div', {'class': 'entry-content'}):
	for li in cl.find_all('li'):
		for lie in li:
			liquor = lie.text.split("(",1)[0][:-1]
			id = lie.text.split("(",1)[1][:-1]
			availableLiquors[liquor] = id

blantonId = [val for key,val in availableLiquors.items() if 'Blanton'.lower() in key.lower()]

if blantonId:
	queryBlanton = requests.post('https://mixblendenjoy.com/wp-content/themes/mixblendenjoy/inc/availability.php', allow_redirects='false', data={
		'location': '83716',
		'nabca': blantonId,
		'name': ''
	})
	newSoup = BeautifulSoup(queryBlanton.text, "html.parser")
	if newSoup.find('li'):
		storeLookup = newSoup.find_all('li')[0]
		closestStore = storeLookup.text.splitlines()[2]
		
		storeInfo = {}
		storeInfo['Store'] = closestStore.split(':',1)[1].split(')',1)[0][1:]+')'
		storeInfo['Address'] = closestStore.split(':',2)[2].split('Phone',1)[0][1:]
		storeInfo['Phone'] = closestStore.split('Phone',1)[1][2:].rstrip()
		storeInfo['Distance'] = closestStore.split('(',2)[2].split(')',1)[0].split('m',1)[0]

		if float(storeInfo['Distance']) <= 20.0:
			print(f'Good News! Blanton\'s is in stock at {storeInfo["Store"]}. Address: {storeInfo["Address"]}')
		else:
			print(f'Blanton\'s is in stock, but {storeInfo["Distance"]} miles away at {storeInfo["Store"]}. Address: {storeInfo["Address"]}...how badly do you want it?' )
	else:
		print("Blanton's is out of stock in Idaho. Sad.")
else:
	print("Blanton's is out of stock in Idaho. Sad.")

