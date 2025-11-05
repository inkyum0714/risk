import json
from data.Symbol import country_code_data_three, country_code_data_five_number, country_airport, country_cities
from flask import Flask, request, render_template, redirect, jsonify
from flask_cors import CORS
from service.exchange import exchange
from service.weather import get_weather
from service.service import find_country_by_city
from service.air_ticket import air_ticket
from service.risk import user_risk
from service.inputvalue import inputvalue_service
import traceback

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", country_code_data_five_number= country_code_data_five_number, airport_names=list(country_airport.keys()), country_code_data_three=country_code_data_three)

@app.route("/inputvalue", methods=["GET", "POST"])
def inputvalue():
    country_cities_number = 0
    user_input_traevel = request.args.get("user_input_traevel")
    print(user_input_traevel)
    user_input_traevel_data = inputvalue_service(user_input_traevel)
    print(user_input_traevel_data)
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
        print(weather_result_list[0][1][0])
        
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



@app.route("/exchange", methods=["GET", "POST"])
def rate():
    base = request.args.get("base")
    print(base)
    exchange_result = exchange(base)
    print({"message": "success","result": exchange_result})
    return jsonify({"message": "success","result": exchange_result})



if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)