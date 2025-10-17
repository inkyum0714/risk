import requests
from data.Symbol import symbol_data, country_code_data_three, country_code_data_two, country_code_data_five_number, country_airport, airport_seat, country_city
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


@app.route("/search", methods=["POST"])
def search():
    user_input_traevel = request.form.get("user_input_traevel", "").strip()
    if user_input_traevel in country_code_data_three:
        user_input_traevel_type = "country"
    elif user_input_traevel in country_airport:
        user_input_traevel_type = "airport"
    elif user_input_traevel in country_code_data_five_number:
        user_input_traevel_type = "city"

    total_score = {}
    weather_result_list= []
    user_input_fromId = request.form.get("fromId", "").strip()
    user_input_toId = request.form.get("toId", "").strip()
    cabinClass = request.form.get("cabinClass", "").strip()
    person_adult = request.form.get("person_adult", "").strip()
    person_children = request.form.get("person_children", "").strip()

    city = request.form.get("country", "").strip()
    user_input_day = request.form.get("user_input_day", "").strip()

    user_input_day = request.form.get("user_input_day", "").strip()
    user_input_traevel = request.form.get("user_input_traevel", "").strip()
    if not user_input_fromId or not user_input_toId:
        return render_template("error.html", message="출발지와 도착지를 모두 입력하세요.")
    if not city or not user_input_day:
        return render_template("error.html", message="날씨 검색 입력이 비어 있습니다.")
    if user_input_traevel in country_code_data_three:
        user_input_traevel_type = "country"
        for continent in country_city:            
            for country in continent["children"]:  
                if country["name"] == user_input_traevel:
                    for city in country["children"]:
                        weather_result_list.append([city , get_weather(city, user_input_day)])
                        airport_result = air_ticket(
                            user_input_fromId,
                            user_input_toId,
                            user_input_day,
                            cabinClass,
                            person_adult,
                            person_children
                        )
                        for i in range(len(airport_result)):
                            total_score[i] = {}
                            score = int(airport_result[i]["총합 점수"]) + float(weather_result_list[i][1]["점수"])
                            total_score[i]["도시"] = city
                            total_score[i]["점수"] = round(score, 0)
                        print(total_score)
    elif user_input_traevel in country_airport:
        user_input_traevel_type = "airport"
        for continent in country_city:  #한국어 공항 입력- city_to_airport - city_en_kr 로 도시 찾고  cluntry_cities에서 도시로 국가 찾기
            for country in continent["children"]:  
                for city in country["children"]:
                    for airport in city["children"]:
                        if airport["name"] == user_input_traevel:
                            weather_result_list.append([city["name"] , get_weather(city["name"], user_input_day)])
                            airport_result = air_ticket(
                                user_input_fromId,
                                user_input_toId,
                                user_input_day,
                                cabinClass,
                                person_adult,
                                person_children
                            )
                            for i in range(len(airport_result)):
                                total_score[i] = {}
                                score = int(airport_result[i]["총합 점수"]) + float(weather_result_list[i][1]["점수"])
                                total_score[i]["도시"] = city["name"]
                                total_score[i]["점수"] = round(score, 0)
                            print(total_score)


    elif user_input_traevel in country_code_data_five_number:
        user_input_traevel_type = "city"
        for city in range():
            if city["name"] == user_input_traevel:



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

