from data.Symbol import country_airport, airport_seat
import requests, json, datetime



def air_ticket(user_input_fromId, user_input_toId, departDate, cabinClass, person_adult, person_children):
    flightDeals_data = []
    air_ticket_result = []
    deal_dic = {}
    url = "https://booking-com15.p.rapidapi.com/api/v1/flights/searchFlights"
    fromId = country_airport[user_input_fromId]
    toId = country_airport[user_input_toId]
    cabinClass = airport_seat[cabinClass]
    try:
        departDate = datetime.datetime.strptime(departDate, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print("⚠ 날짜 형식이 잘못되었습니다. 올바른 예: 20251006")
    print(fromId, toId, departDate, cabinClass, person_adult, person_children)
    querystring = {"fromId": f"{fromId}.AIRPORT","toId":f"{toId}.AIRPORT",
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
                        # 위탁수하물 정보가 존재할 때만 추가
                        checked_luggage = response_data["data"]["flightOffers"][j]["segments"][0].get("travellerCheckedLuggage", [])
                        if len(checked_luggage) >= 1:
                            try:
                                weight_kg = checked_luggage[0]["luggageAllowance"]["maxWeightPerPiece"] * 0.45359237
                            except KeyError:
                                weight_kg = "0"
                        else: weight_kg = "0"
                        deal_dic["위탁수하물 용량"] = round(float(weight_kg), 0)
                        cabin_luggage = response_data["data"]["flightOffers"][j]["segments"][0].get("travellerCabinLuggage", [])
                        if cabin_luggage and "luggageAllowance" in cabin_luggage[0]:
                           deal_dic["기내수하물 용량"] = (
                                   round(
                                       int(cabin_luggage[0]["luggageAllowance"]["maxWeightPerPiece"]) * 0.45359237,
                                       0
                                   )
                               )
                        deal_dic["총합 점수"] = 1000000 / (int(deal_dic["가격"]) / (int(person_adult)) + int(person_children) * 0.75)+ int(deal_dic["위탁수하물 용량"]) + int(deal_dic["기내수하물 용량"]) * 1.5 
                        air_ticket_result.append(deal_dic)


    print(air_ticket_result)
    with open("flights_result.json", "w", encoding="utf-8") as f:
        json.dump(air_ticket_result, f, ensure_ascii=False, indent=4)
    return air_ticket_result      