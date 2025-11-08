import json, os
def inputvalue_service(user_input_traevel):
    country_cities_number = 0
    translation_result = "translation_result.json"
    country_airport = os.path.join("data", "country_airport.json")
    country_cities = os.path.join("data", "country_cities.json")
    country_code_data_five = os.path.join("data", "country_code_data_five.json")
    country_code_data_three = os.path.join("data", "country_code_data_three.json")
    with open(translation_result, "r", encoding="utf-8") as f:
        krkr_airport = json.load(f)
    with open(country_airport, "r", encoding="utf-8") as f:
        country_airport = json.load(f)
    with open(country_cities, "r", encoding="utf-8") as f:
        country_cities = json.load(f)
    with open(country_code_data_five, "r", encoding="utf-8") as f:
        country_code_data_five_number = json.load(f)
    with open(country_code_data_three, "r", encoding="utf-8") as f:
        country_code_data_three_number = json.load(f)     
    user_input_traevel_data = {
        "country": "",
        "city": [],
        "airport": []
    }
    print(user_input_traevel)
    if user_input_traevel in country_code_data_three_number: #나라
        user_input_traevel_type = "country"
        print(user_input_traevel_type)
        user_input_traevel_data["country"] = user_input_traevel
        for i in range(len(country_cities[0]["children"])):
            if country_cities[0]["children"][i]["name"] == user_input_traevel:
                print("옴")
                for j in range(len(country_cities[0]["children"][i]["children"])):
                    user_input_traevel_data["city"].append(country_cities[0]["children"][i]["children"][j]["name"])
        country_cities_number = 0
        for key, value in krkr_airport.items():
            for city in user_input_traevel_data["city"]:
                if value == city:
                    user_input_traevel_data["airport"].append(key)
        return user_input_traevel_data

    elif user_input_traevel in country_airport: #공항
        user_input_traevel_type = "airport"
        print(user_input_traevel_type)
        for i in range(len(country_cities[0]["children"])):
            for j in range(len(country_cities[0]["children"][i]["children"])):
                if country_cities[0]["children"][i]["children"][j]["name"] == krkr_airport[user_input_traevel]:
                    user_input_traevel_data["country"] = country_cities[0]["children"][i]["name"]
                    break
        user_input_traevel_data["city"] = [krkr_airport[user_input_traevel]]
        user_input_traevel_data["airport"] = user_input_traevel
        return user_input_traevel_data
    
    elif user_input_traevel in country_code_data_five_number: #도시
        user_input_traevel_type = "city"
        print(user_input_traevel_type)
        for i in range(len(country_cities[0]["children"])):
            for j in range(len(country_cities[0]["children"][i]["children"])):
                if country_cities[0]["children"][i]["children"][j]["name"] == user_input_traevel:
                    user_input_traevel_data["country"] = country_cities[0]["children"][i]["name"]
                    break
        for key, value in krkr_airport.items():
            if value == user_input_traevel:
                user_input_traevel_data["airport"].append(key)
                country_cities_number += 1
        user_input_traevel_data["city"] = [user_input_traevel]
        return user_input_traevel_data
