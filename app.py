import requests, os, json
from data.Symbol import symbol_data, country_code_data_three, country_code_data_two, country_code_data_five_number, country_airport, country_cities
from flask import Flask, request, render_template, redirect
from service.exchange import exchange
from service.weather import get_weather
from service.service import find_country_by_city
from service.air_ticket import air_ticket
from service.risk import user_risk
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
    total_score = {}
    weather_result_list= []
    airport_result = []
    cabinClass = "이코노미"
    json_true_false = False
    error_num = 0
    user_input_traevel = request.form.get("user_input_traevel", "").strip() #어디갈지
    user_input_day = request.form.get("user_input_day", "").strip() #날짜
    if user_input_traevel in country_code_data_three: #나라
        user_input_traevel_type = "country"
    elif user_input_traevel in country_airport: #공항
        user_input_traevel_type = "airport"
    elif user_input_traevel in country_code_data_five_number: #도시
        user_input_traevel_type = "city"
    translation_result = "translation_result.json"#얘는 한국어 공항과 한국어 도시를 해주는
    user_request_query = "user_requset_query.json"
    # 2. JSON 파일 읽기
    with open(translation_result, "r", encoding="utf-8") as f:
        krkr_airport = json.load(f)
    #with open(user_request_query, "r", encoding="utf-8") as f:
    #   krkr_airport = json.load(f) 
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

    #     당장 할 수 있는 것은.
    # 사용자가 n이라는 국가로 query를 날리면.... 
    # 그 국가에 대한 점수를 쿼리하는데,
    # 최종적으로 나온 점수를. 그냥 저장 때려버리기. (JSON으로.)
    
    # 그리고 다음번에 다시 그 국가로 query를 날리면, 있는 정보는 JSON에서 가져오고 바로.
    # 없으면 새로 받아오기. 

    user_input_traevel_shift_city_list = []
    if user_input_traevel_type == "country":
        for continent in country_cities:
            for country in continent["children"]:
                for i in range(len(country["children"])):
                    if country["children"][i]["groupNm"] == user_input_traevel:
                        user_input_traevel_city_country = country["name"]
                        if user_input_traevel == country["children"][i]["groupNm"]:
                            user_input_traevel_shift_city_list.append(country["children"][i]["name"])
                            # 올바른 구조
                            weather_result_list.append([user_input_traevel_shift_city_list[i], get_weather(user_input_traevel_shift_city_list[i], user_input_day)])

                            found_key = None
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
                            risk_score = user_risk(user_input_traevel)
                            print(weather_result_list)
                            weather_score = float(weather_result_list[0][1].split(':')[1].strip())
                            score = int(airport_result[0]["총합 점수"]) + weather_score - risk_score  # 항상 첫 번째 요소 사용
                            total_score[i] = {}
                            total_score[i]["도시"] = user_input_traevel_shift_city_list[i]
                            total_score[i]["사용할_항공사"] = airport_result[0]["항공사 이름"]
                            total_score[i]["점수"] = round(score, 0)
                            print(total_score)

        print(total_score)
        return render_template("search.html", total_scores = total_score, weather_result_list = weather_result_list,
                                                airport_results = airport_result)
    elif user_input_traevel_type == "airport":
        print("입력값: ", user_input_traevel_type)
        for airport in krkr_airport:
            if airport == user_input_traevel:
                print(user_input_traevel)
                user_input_traevel_shift_city = krkr_airport[user_input_traevel]
                weather_result_list.append([user_input_traevel , get_weather(user_input_traevel_shift_city, user_input_day)])
                print(weather_result_list)
                found_key = None
                toId = user_input_traevel
                airport_result = air_ticket(
                        toId,
                        user_input_day,
                        cabinClass,
                    )
                print(airport_result)
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

