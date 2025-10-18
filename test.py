import requests

url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

querystring = {"fromId":"ICN.AIRPORT","toId":"LGA.AIRPORT","departDate":"2025-10-19","stops":"none","pageNo":"1","adults":"1","children":"0","sort":"BEST","cabinClass":"ECONOMY","currency_code":"ICN"}

headers = {
	"x-rapidapi-key": "b04b637a2amshcc217bbf80f6ec3p193dd6jsndf23126efc51",
	"x-rapidapi-host": "booking-com15.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())