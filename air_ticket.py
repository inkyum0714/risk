import requests

url = "https://booking-com15.p.rapidapi.com/api/v1/flights/getMinPriceMultiStops"

querystring = {"legs":"[{'fromId':'BOM.AIRPORT','toId':'AMD.AIRPORT','date':'2024-05-25'},{'fromId':'AMD.AIRPORT','toId':'BOM.AIRPORT','date':'2024-05-26'}]","cabinClass":"FIRST","currency_code":"AED"}

headers = {
	"x-rapidapi-key": "dd019e6396msh5b4c8d6763bb299p145742jsn20b7704bf7ae",
	"x-rapidapi-host": "booking-com15.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())