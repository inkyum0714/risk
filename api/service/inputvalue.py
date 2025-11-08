import json, os
def inputvalue_service(user_input_travel):
    country_cities_number = 0
    current_dir = os.path.dirname(__file__)  # inputvalue.py가 있는 폴더(api/service)

    # data 폴더에 있는 json 파일 경로 지정
    country_airport_path = os.path.join(current_dir, "..", "data", "country_airport.json")
    country_cities_path = os.path.join(current_dir, "..", "data", "country_cities.json")
    country_code_data_five_path = os.path.join(current_dir, "..", "data", "country_code_data_five.json")
    country_code_data_three_path = os.path.join(current_dir, "..", "data", "country_code_data_three.json")
    translation_result_path = os.path.join(current_dir, "..", "translation_result.json")

    # JSON 파일 읽기
    with open(translation_result_path, "r", encoding="utf-8") as f:
        krkr_airport = json.load(f)

    with open(country_airport_path, "r", encoding="utf-8") as f:
        country_airport = json.load(f)

    with open(country_cities_path, "r", encoding="utf-8") as f:
        country_cities = json.load(f)

    with open(country_code_data_five_path, "r", encoding="utf-8") as f:
        country_code_data_five_number = json.load(f)

    with open(country_code_data_three_path, "r", encoding="utf-8") as f:
        country_code_data_three_number = json.load(f) 
    user_input_travel_data = {
        "country": "",
        "city": [],
        "airport": []
    }
    print(user_input_travel)
    if user_input_travel in country_code_data_three_number: #나라
        user_input_travel_type = "country"
        print(user_input_travel_type)
        user_input_travel_data["country"] = user_input_travel
        for i in range(len(country_cities[0]["children"])):
            if country_cities[0]["children"][i]["name"] == user_input_travel:
                print("옴")
                for j in range(len(country_cities[0]["children"][i]["children"])):
                    user_input_travel_data["city"].append(country_cities[0]["children"][i]["children"][j]["name"])
        country_cities_number = 0
        for key, value in krkr_airport.items():
            for city in user_input_travel_data["city"]:
                if value == city:
                    user_input_travel_data["airport"].append(key)
        return user_input_travel_data

    elif user_input_travel in country_airport: #공항
        user_input_travel_type = "airport"
        print(user_input_travel_type)
        for i in range(len(country_cities[0]["children"])):
            for j in range(len(country_cities[0]["children"][i]["children"])):
                if country_cities[0]["children"][i]["children"][j]["name"] == krkr_airport[user_input_travel]:
                    user_input_travel_data["country"] = country_cities[0]["children"][i]["name"]
                    break
        user_input_travel_data["city"] = [krkr_airport[user_input_travel]]
        user_input_travel_data["airport"] = user_input_travel
        return user_input_travel_data
    
    elif user_input_travel in country_code_data_five_number: #도시
        user_input_travel_type = "city"
        print(user_input_travel_type)
        for i in range(len(country_cities[0]["children"])):
            for j in range(len(country_cities[0]["children"][i]["children"])):
                if country_cities[0]["children"][i]["children"][j]["name"] == user_input_travel:
                    user_input_travel_data["country"] = country_cities[0]["children"][i]["name"]
                    break
        for key, value in krkr_airport.items():
            if value == user_input_travel:
                user_input_travel_data["airport"].append(key)
                country_cities_number += 1
        user_input_travel_data["city"] = [user_input_travel]
        return user_input_travel_data
