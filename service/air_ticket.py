from data.Symbol import country_airport, airport_seat
import requests
import json


def air_ticket(user_input_fromId, user_input_toId, departDate, cabinClass, person_adult, person_children):
    flightDeals_data = []
    air_ticket_result = []
    deal_dic = {}
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"
    fromId = country_airport[user_input_fromId]
    toId = country_airport[user_input_toId]
    cabinClass = airport_seat[cabinClass]
    querystring = {"fromId":{fromId},"toId":{toId},
                   "stops":"none","pageNo":"1","adults":{person_adult},
                   "children":{person_children},"sort":"BEST",
                   "cabinClass":{cabinClass},"currency_code":"KRW", "departDate":{departDate}}


    headers = {
    	"x-rapidapi-host":"booking-com15.p.rapidapi.com",
    	"x-rapidapi-key": "44b53a7a9fmshd4b09e186aeeefbp1eb70ejsnbca7d65497bd"
    }

    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json() 
    for i in range(3):  
        deals = response_data["data"]["flightDeals"][i]["price"]
        flightDeals_data.append(deals)
        token = response_data["data"]["flightDeals"][i]["offerToken"]
        for j in range(len(response_data["data"]["flightOffers"])):
            if token == response_data["data"]["flightOffers"][j]["token"]:
                for k in range(len(response_data["data"]["aggregation"]["airlines"])):
                    if response_data["data"]["aggregation"]["airlines"][k]["minPrice"]["units"] == response_data["data"]["flightDeals"][i]["price"]["units"]:
                        deal_dic = {}
                        deal_dic["항공사 이름"] = response_data["data"]["aggregation"]["airlines"][k]["name"]
                        deal_dic["가격"] = response_data["data"]["flightDeals"][i]["price"]["units"]
                        deal_dic["탑승 나라"] = response_data["data"]["flightOffers"][j]["segments"][0]["departureAirport"]["countryName"]
                        deal_dic["도착 나라"] = response_data["data"]["flightOffers"][j]["segments"][0]["arrivalAirport"]["countryName"]
                        deal_dic["최초 탑승 시간"] = response_data["data"]["flightOffers"][j]["segments"][0]["departureTime"]
                        deal_dic["마지막 탑승 시간"] = response_data["data"]["flightOffers"][j]["segments"][0]["arrivalTime"]
                        deal_dic["위탁수하물 용량"] = str(round(response_data["data"]["flightOffers"][j]["segments"][0]["travellerCheckedLuggage"][0]["luggageAllowance"]["maxWeightPerPiece"] * 0.45359237, 3)) + "kg"                           
                        deal_dic["기내수하물 용량"] = str(round(response_data["data"]["flightOffers"][j]["segments"][0]["travellerCabinLuggage"][0]["luggageAllowance"]["maxWeightPerPiece"] * 0.45359237, 3)) + "kg"
                        air_ticket_result.append(deal_dic)

    print(air_ticket_result)
    with open("flights.json", "w", encoding="utf-8") as f:
        json.dump(air_ticket_result, f, ensure_ascii=False, indent=4)