import requests
import json

url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"

querystring = {
    "fromId":"GMP.AIRPORT",
    "toId":"CJU.AIRPORT",
    "departDate":"2025-10-06",
    "stops":"none",
    "pageNo":"1",
    "adults":"1",
    "sort":"BEST",
    "cabinClass":"ECONOMY",
    "currency_code":"KRW"
}

headers = {
    "x-rapidapi-key": "dd019e6396msh5b4c8d6763bb299p145742jsn20b7704bf7ae",
    "x-rapidapi-host": "booking-com15.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

data = response.json()

with open("flights.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("flights.json 파일로 저장 완료!")
