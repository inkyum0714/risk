import requests
from data.Symbol import symbol_data, country_code_data_three, country_code_data_two, country_code_data_five_number, country_airport, airport_seat
from flask import Flask, request, render_template, redirect
from service.exchange import exchange
from service.weather import get_weather
from service.service import find_country_by_city
from service.air_ticket import air_ticket
app = Flask(__name__)

RISK_API_KEY = "jiDRCL1%2FKFqcHeMt6Q8%2FwIFNhQoj79XSfFhNpfZCeNWBmGu8oDp%2B7P0gPHWcCr96h1YrqMtF2QGeyMItKFO%2FTA%3D%3D"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", country_code_data_five_number= country_code_data_five_number, airport_names=list(country_airport.keys()))

@app.route('/main', methods=['GET', 'POST'])
def risk():
    risk_data = None
    if request.method == 'POST':
        country_risk = request.form.get('riskmap', '').strip()
        country = country_code_data_two[country_risk]
        url = f"https://apis.data.go.kr/1262000/TravelAlarmService2/getTravelAlarmList2?serviceKey={RISK_API_KEY}&returnType=JSON&numOfRows=1&cond[country_iso_alp2::EQ]={country}"
        
        response = requests.get(url)
        if response.status_code == 200:
            try:
                data = response.json()
                risk_data  = data['response']['body']['items']['item'][0]['alarm_lvl']
                print("위험경보수준: " + risk_data)
            except Exception as e:
                print("JSON 파싱 실패:", e)
                print("원본 텍스트:", response.text)
                print(response.status_code)
                print(f"입력값 확인: '{country_risk}'") 
        else:
            print("Error:", response.text)

    return render_template('main.html', risks=[risk_data] if risk_data else None)

@app.route('/air', methods = ['GET', 'POST'])
def air():
    if request.method == 'POST':
        user_input_fromId = request.form.get('fromId"', '').strip()
        user_input_toId = request.form.get('toId', '').strip()
        departDate = request.form.get('departDate', '').strip()
        cabinClass = request.form.get('cabinClass', '').strip()
        person_adult = request.form.get('person_adult', '').strip()
        person_children = request.form.get('person_children', '').strip()
        return render_template('main.html', user_input_toId = user_input_toId, user_input_fromId = user_input_fromId, departDate = departDate, cabinClass = cabinClass, person_adult = person_adult, person_children = person_children)


@app.route("/search_weather", methods=["POST"])
def search_weather():
    city = request.form.get("country", "").strip()
    user_input_day = request.form.get("user_input_day", "").strip()

    if not city or not user_input_day:
        return render_template("error.html", message="날씨 검색 입력이 비어 있습니다.")

    weather_result = get_weather(city, user_input_day)
    country = find_country_by_city(city)
    exchange_result = exchange("대한민국", country, "10000")

    return render_template(
        "search.html",
        weather_results=weather_result,
        exchange_results=exchange_result,
        country_code_data_five_number=country_code_data_five_number,
        airport_names=list(country_airport.keys())
    )


@app.route("/search_flight", methods=["POST"]) #점수 형식: 기본적으로 반비례. 가격 - 25만원에 가까울. 가격 점수 = (25,000,000 / 가격) * 2 / 5. 위탁수하물 점수 = 
def search_flight():
    user_input_fromId = request.form.get("fromId", "").strip()
    user_input_toId = request.form.get("toId", "").strip()
    departDate = request.form.get("departDate", "").strip()
    cabinClass = request.form.get("cabinClass", "").strip()
    person_adult = request.form.get("person_adult", "").strip()
    person_children = request.form.get("person_children", "").strip()

    if not user_input_fromId or not user_input_toId:
        return render_template("error.html", message="출발지와 도착지를 모두 입력하세요.")
    airport_result = air_ticket(
        user_input_fromId,
        user_input_toId,
        departDate,
        cabinClass,
        person_adult,
        person_children,
    )
    for i in range(len(airport_result)):
        air_socre = 10000000 / airport_result[i]["가격"] + airport_result[i]["위탁수하물 용량"] * 20 
    return render_template(
        "search.html",
        airport_results=airport_result,
        country_code_data_five_number=country_code_data_five_number,
        airport_names=list(country_airport.keys())
    )ㄷ
    
@app.route("/exchange", methods=["POST"])
def rate():
    user_base = request.form.get("base", "").strip()
    user_currencies = request.form.get("currencies", "").strip()
    amount = request.form.get("amount", "").strip()
    exchange_result = exchange(user_base, user_currencies, amount)
    return render_template("main.html", exchange_results=exchange_result)



@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        user_input_day = request.form.get('user_input_day', '').strip()
        user_input_country = request.form.get('country', '').strip() 
        weather_result = get_weather(user_input_country, user_input_day)
    return render_template("main.html", weather_results=weather_result)

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)

