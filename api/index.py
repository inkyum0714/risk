import json, os, sys
from api.data.Symbol import country_code_data_three, country_code_data_five_number, country_airport
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from api.service.exchange import exchange
from api.service.weather import get_weather
from api.service.air_ticket import air_ticket
from api.service.risk import user_risk
from api.service.inputvalue import inputvalue_service

print("Python path:", sys.path)  # 디버그용

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html",
        country_code_data_five_number=country_code_data_five_number,
        airport_names=list(country_airport.keys()),
        country_code_data_three=country_code_data_three
    )

@app.route("/search", methods=["GET", "POST"])
def search():
    print("ZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
    user_input_travel = request.args.get("user_input_travel")
    print(user_input_travel)
    user_input_travel_data = inputvalue_service(user_input_travel)
    return jsonify({"message": "success", "result": user_input_travel_data})

@app.route("/weather", methods=["GET", "POST"])
def weather():
    try:
        sum_score = 0   
        weather_result_list = []
        user_input_travel_city = request.args.get("user_input_travel_city")
        user_input_day = request.args.get("date")
        cities = user_input_travel_city.split(",")
        for city in cities:
            weather_result_list.append([
                city,
                get_weather(city.strip(), user_input_day)
            ])
        print("나옴")
        sum_score = sum(weather_result_list[0][1][0])
        total_weather_score = sum_score / len(weather_result_list[0][1][0])
        return jsonify({
            "message": "success",
            "result_list": weather_result_list,
            "result": round(total_weather_score)
        })
    except Exception as e:
        print("예외 발생:", e)
        return jsonify({"message": "error", "result": "외부 서버에서 응답하지 않습니다"})

@app.route("/airticket", methods=["GET", "POST"])
def airticket():
    try:
        current_dir = os.path.dirname(__file__)
        translation_result_path = os.path.join(current_dir, "..", "translation_result.json")
        translation_result_path = os.path.abspath(translation_result_path)
        with open(translation_result_path, "r", encoding="utf-8") as f:
            krkr_airport = json.load(f)
            print("난데 와케룬다요~")
        user_input_travel_city = request.args.get("user_input_travel_city")
        user_input_day = request.args.get("date")

        found_key = None    
        for key, value in krkr_airport.items():
            if value.strip().lower() == user_input_travel_city.lower():
                found_key = key
                toId = key
                break

        if found_key is None:
            return jsonify({"message": "error", "result": "0"})
        airport_result = air_ticket(toId, user_input_day)
        airport_result_score = airport_result[0]["총합 점수"]
        return jsonify({
            "message": "success",
            "result": round(airport_result_score, 1),
            "result_data": airport_result
        })
    except Exception as e:
        print("예외 발생:", e)
        return jsonify({"message": "error", "result": "응답하지 않습니다"})

@app.route("/risk", methods=["GET", "POST"])
def risk():
    user_input_travel_country = request.args.get("user_input_travel_country")
    risk_data = user_risk(user_input_travel_country)
    return jsonify({"message": "success", "result": risk_data})

@app.route("/total", methods=["GET", "POST"])
def total():
    try:
        weather = float(request.args.get('weather', 0))
        air_ticket_score = float(request.args.get('air_ticket', 0))
        risk = float(request.args.get('risk', 0))
        total_data = round((30 + air_ticket_score - risk - weather)) 
        return jsonify({"message": "success", "result": total_data})
    except ValueError:
        return jsonify({"message": "error", "result": 0})

@app.route("/exchange", methods=["GET", "POST"])
def rate():
    base = request.args.get("base")
    exchange_result = exchange(base)
    return jsonify({
        "message": "success",
        "result": exchange_result[0],
        "symbol": exchange_result[1]
    })

