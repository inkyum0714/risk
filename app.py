import requests, os, json, time
from data.Symbol import symbol_data, country_code_data_three, country_code_data_two, country_code_data_five_number, country_airport, country_cities
from flask import Flask, request, render_template, redirect, jsonify
from flask_cors import CORS
from service.exchange import exchange
from service.weather import get_weather
from service.service import find_country_by_city
from service.air_ticket import air_ticket
from service.risk import user_risk
import traceback

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", country_code_data_five_number= country_code_data_five_number, airport_names=list(country_airport.keys()), country_code_data_three=country_code_data_three)

@app.route("/inputvalue", methods=["GET", "POST"])
def inputvalue():
    airport_result = []
    json_true_false = False
    error_num = 0
    country_cities_number = 0
    user_input_traevel = request.args.get("user_input_traevel")
    user_input_day = request.form.get("user_input_day", "").strip() #날짜
    translation_result = "translation_result.json"#얘는 한국어 공항과 한국어 도시를 해주는
    user_request_query = "user_requset_query.json"
    # 2. JSON 파일 읽기
    with open(translation_result, "r", encoding="utf-8") as f:
        krkr_airport = json.load(f)
    user_input_traevel_data = {
        "country": "",
        "city": [],
        "airport": []
    }
    user_total_city_data = {}
    if user_input_traevel in country_code_data_three: #나라
        user_input_traevel_type = "country"
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
        return jsonify({"message": "success", "result": user_input_traevel_data})


    elif user_input_traevel in country_airport: #공항
        user_input_traevel_type = "airport"
        for i in range(len(country_cities[0]["children"])):
            for j in range(len(country_cities[0]["children"][i]["children"])):
                if country_cities[0]["children"][i]["children"][j]["name"] == krkr_airport[user_input_traevel]:
                    user_input_traevel_data["country"] = country_cities[0]["children"][i]["name"]
                    break
        user_input_traevel_data["city"] = [krkr_airport[user_input_traevel]]
        user_input_traevel_data["airport"] = user_input_traevel
        return jsonify({"message": "success", "result": user_input_traevel_data})


    elif user_input_traevel in country_code_data_five_number: #도시
        user_input_traevel_type = "city"
        for i in range(len(country_cities[0]["children"])):
            for j in range(len(country_cities[0]["children"][i]["children"])):
                if country_cities[0]["children"][i]["children"][j]["name"] == user_input_traevel:
                    user_input_traevel_data["country"] = country_cities[0]["children"][i]["name"]
                    break
        found_key = None
        for key, value in krkr_airport.items():
            if value == user_input_traevel:
                found_key = key
                user_input_traevel_data["airport"].append(key)
                country_cities_number += 1
        user_input_traevel_data["city"] = [user_input_traevel]
        return jsonify({"message": "success", "result": user_input_traevel_data})
        
@app.route("/weather", methods=["GET", "POST"])
def weather():
    try:
        sum_score = 0
        translation_result = "translation_result.json"
        weather_result_list= []
        user_input_traevel_city = request.args.get("user_input_traevel_city")
        user_input_day = request.args.get("date")
        cities = user_input_traevel_city.split(",")
        for city in cities:
            weather_result_list.append([
                city,
                get_weather(city.strip(), user_input_day)
            ])
        sum_score = sum(weather_result_list[0][1][0])
        total_weather_score = sum_score / len(weather_result_list[0][1][0])
        return jsonify({"message": "success","result_list": weather_result_list, "result": round(total_weather_score)})
    except Exception as e:
        print("예외 발생!")
        print("예외 타입:", type(e))         # 예외 종류
        print("예외 메시지:", e)            # 예외 메시지
        print("트레이스백 상세:")
        traceback.print_exc()  
        return jsonify({"message": "success","result": "외부 서버에서 응답하지 않습니다"})

@app.route("/airticket", methods=["GET", "POST"])
def airticket():
    try:
        print("왔음")
        translation_result = "translation_result.json"
        with open(translation_result, "r", encoding="utf-8") as f:
            krkr_airport = json.load(f)

        user_input_traevel_city = request.args.get("user_input_traevel_city")
        user_input_day = request.args.get("date")

        found_key = None    
        for key, value in krkr_airport.items():
            if value.strip().lower() == user_input_traevel_city.lower():
                found_key = key
                toId = key
                break

        if found_key is None:
            return jsonify({"message": "error", "result": "0"})

        airport_result = air_ticket(toId, user_input_day)
        airport_result_score = airport_result[0]["총합 점수"]
        print("항공권 끝남")
        print(airport_result)
        return jsonify({"message": "success","result": round(airport_result_score, 1), "result_data": airport_result})
    except:
        return jsonify({"message": "success","result": "응답하지 않습니다"})

@app.route("/risk", methods=["GET", "POST"])
def risk():
    print("위험도 도착")
    user_input_traevel_country = request.args.get("user_input_traevel_country")
    risk_data = user_risk(user_input_traevel_country)
    print("위험도 끝남")
    return jsonify({"message": "success","result": risk_data})

@app.route("/total", methods=["GET", "POST"])
def total():
    try:
        print("총합 점수 계산 도착")
        weather = float(request.args.get('weather', 0))
        air_ticket = float(request.args.get('air_ticket', 0))
        risk = float(request.args.get('risk', 0))
        print(weather, air_ticket, risk)
        total_data = round((30 + air_ticket - risk- weather)) 
        print(total_data)
        return jsonify({"message": "success","result": total_data})
    except ValueError:
        return jsonify({"message": "error", "result": 0})



@app.route("/exchange", methods=["POST"])
def rate():
    user_base = request.form.get("base", "").strip()
    user_currencies = request.form.get("currencies", "").strip()
    amount = request.form.get("amount", "").strip()
    exchange_result = exchange(user_base, user_currencies, amount)
    return render_template("main.html", exchange_results=exchange_result)



if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)

