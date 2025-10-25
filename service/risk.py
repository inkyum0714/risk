import json

def user_risk(user_input_country):
    risk_data_score = 0
    risk_data = "risk_data.json"

    with open(risk_data, "r", encoding="utf-8") as f:
        risk_data = json.load(f)
    for i in range(len(risk_data)):
        if risk_data[i]["ntnNm"] == user_input_country:
            if risk_data[i]["alertNm"] == "Y":
                risk_data_score += 5
            if risk_data[i]["alertCt"] == "Y":
                risk_data_score += 7
            if risk_data[i]["alertRc"] == "Y":
                risk_data_score += 5
            if risk_data[i]["alertBn"] == "Y":
                risk_data_score += 10
            if risk_data[i]["alertAl"] == "Y":
                risk_data_score += 3                   
    return risk_data_score




    #for i in range(user_request_query):
    #    if user_input_traevel == user_request_query[i]:
    #        json_true_false = True
    # if user_input_traevel_type == "country":
    #     cons = country_cities[0]["children"]
    #     for i in range(len(cons)):
    #         if cons[i]['name'] == user_input_traevel:
    #             cities_name = []
    #             for city in cons[i]['childeren']:
    #                 cities_name.append(city['name'])
    #     for city in cities_name:
    #         ap_name = [key for key, value in krkr_airport.items() if value == city]
    #         weather = get_weather(city,user_input_day)
