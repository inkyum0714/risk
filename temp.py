import requests

url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

querystring = {"fromId":"ICN.AIRPORT","toId":"FUK.AIRPORT","departDate":"2025-10-14","pageNo":"1","adults":"1","children":"1","sort":"CHEAPEST","cabinClass":"ECONOMY"}

headers = {
    	"x-rapidapi-host":"booking-com15.p.rapidapi.com",
    	"x-rapidapi-key": "44b53a7a9fmshd4b09e186aeeefbp1eb70ejsnbca7d65497bd"
    }

response = requests.get(url, headers=headers, params=querystring)

print(response.json())      