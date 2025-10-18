import requests, os, json
from data.Symbol import symbol_data, country_code_data_three, country_code_data_two, country_code_data_five_number, country_airport, country_cities
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



@app.route("/search", methods=["POST"])
def search():
    user_input_traevel = request.form.get("user_input_traevel", "").strip() #어디갈지
    user_input_day = request.form.get("user_input_day", "").strip() #날짜
    if user_input_traevel in country_code_data_three: #나라
        user_input_traevel_type = "country"
    elif user_input_traevel in country_airport: #공항
        user_input_traevel_type = "airport"
    elif user_input_traevel in country_code_data_five_number: #도시
        user_input_traevel_type = "city"
    total_score = {}
    weather_result_list= []
    airport_result = []
    cabinClass = "이코노미"
    translation_result = "translation_result.json" #얘는 한국어 공항과 한국어 도시를 해주는
    # 2. JSON 파일 읽기
    with open(translation_result, "r", encoding="utf-8") as f:
        krkr_airport = json.load(f) #얘 
    
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



    user_input_traevel_shift_city_list = []
    if user_input_traevel_type == "country":
        for continent in country_cities:
            for country in continent["children"]:
                for i in range(len(country["children"])):
                    if country["children"][i]["groupNm"] == user_input_traevel:
                        user_input_traevel_city_country = country["name"]
                        if user_input_traevel == country["children"][i]["groupNm"]:
                            user_input_traevel_shift_city_list.append(country["children"][i]["name"])
                            weather_result_list.append([user_input_traevel , get_weather(user_input_traevel_shift_city_list[i], user_input_day)])
                            found_key = None
                            print(user_input_traevel_shift_city_list[i])
                            for key, value in krkr_airport.items():
                                if value == user_input_traevel_shift_city_list[i]:
                                    found_key = key
                                    toId = key
                                    break
                            airport_result = air_ticket(
                                    toId,
                                    user_input_day,
                                    cabinClass,
                                )
                            try:
                                if airport_result:  # 결과가 있을 때만
                                    weather_score = float(weather_result_list[0][1].split(':')[1].strip())
                                    score = int(airport_result[0]["총합 점수"]) + weather_score  # 항상 첫 번째 요소 사용
                                    total_score[i] = {}
                                    total_score[i]["도시"] = user_input_traevel_shift_city_list[i]
                                    total_score[i]["사용할_항공사"] = airport_result[0]["항공사 이름"]
                                    total_score[i]["점수"] = round(score, 0)
                                print(total_score)
                            except:
                                total_score["도시"] = user_input_traevel_shift_city_list[i]
                                total_score["사용할_항공사"] = "존재하지 않습니다."
                                total_score["점수"] = "존재하지 않습니다."
                                error_num += 1
        total_score = {k: v for k, v in total_score.items() if k < 30}
        total_score = dict(sorted(total_score.items(), key=lambda item: item[1]['점수'], reverse=True))
        return render_template("search.html", total_scores = total_score, weather_result_list = weather_result_list,
                                                airport_results = airport_result)
    elif user_input_traevel_type == "airport":
        for continent in country_cities:
            for country in continent["children"]:
                for i in range(len(country["children"])):
                    if country["children"][i]["name"] == user_input_traevel:
                        user_input_traevel_city_country = country["name"]
                        weather_result_list.append([user_input_traevel , get_weather(user_input_traevel, user_input_day)])
                        found_key = None
                        for key, value in krkr_airport.items():
                            if value == user_input_traevel:
                                found_key = key
                                toId = key
                                break
                        airport_result = air_ticket(
                                toId,
                                user_input_day,
                                cabinClass,
                            )
                        for i in range(len(airport_result)):
                            total_score[i] = {}
                            # i번째 도시의 날씨 점수 사용
                            weather_score = float(weather_result_list[0][1].split(':')[1].strip())
                            score = int(airport_result[i]["총합 점수"]) + weather_score
                            total_score[i]["도시"] = user_input_traevel
                            total_score[i]["사용할_항공사"] = airport_result[i]["항공사 이름"]
                            total_score[i]["점수"] = round(score, 0)
                        print(total_score)
                        return render_template("search.html", total_scores = total_score, weather_result_list = weather_result_list,
                                               airport_results = airport_result)

    elif user_input_traevel_type == "city":
        for continent in country_cities:
            for country in continent["children"]:
                for i in range(len(country["children"])):
                    if country["children"][i]["name"] == user_input_traevel:
                        user_input_traevel_city_country = country["name"]
                        weather_result_list.append([user_input_traevel , get_weather(user_input_traevel, user_input_day)])
                        found_key = None
                        for key, value in krkr_airport.items():
                            if value == user_input_traevel:
                                found_key = key
                                toId = key
                                break
                        airport_result = air_ticket(
                                toId,
                                user_input_day,
                                cabinClass,
                            )
                        for i in range(len(airport_result)):
                            total_score[i] = {}
                            # i번째 도시의 날씨 점수 사용
                            weather_score = float(weather_result_list[0][1].split(':')[1].strip())
                            score = int(airport_result[i]["총합 점수"]) + weather_score
                            total_score[i]["도시"] = user_input_traevel
                            total_score[i]["사용할_항공사"] = airport_result[i]["항공사 이름"]
                            total_score[i]["점수"] = round(score, 0)
                        print(total_score)
    return render_template("search.html", total_scores = total_score, weather_result_list = weather_result_list,
                                               airport_results = airport_result)
    





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

