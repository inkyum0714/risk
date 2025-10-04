import requests
from data.Symbol import symbol_data, country_code_data_three, country_code_data_two, country_code_data_five_number
from flask import Flask, request, render_template
from service.exchange import exchange
from service.weather import get_weather
from service.service import find_country_by_city

app = Flask(__name__)

EXCHANGE_API_KEY = "fxr_live_0e9f7bba09e36d62b800cfea2147bdd6efaf"
WEATHER_API_KEY = "lfwWiH5cTMe8Foh-XJzH6g"
RISK_API_KEY = "jiDRCL1%2FKFqcHeMt6Q8%2FwIFNhQoj79XSfFhNpfZCeNWBmGu8oDp%2B7P0gPHWcCr96h1YrqMtF2QGeyMItKFO%2FTA%3D%3D"

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", country_code_data_five_number= country_code_data_five_number)

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

@app.route("/search", methods = ['POST'])
def search():
    if request.method == 'POST':
        city = request.form.get('country', '').strip()
        date = request.form.get('travel_date', '').strip()
        weather_result = get_weather(city, date)
        country = find_country_by_city(country)
        exchange_result = exchange("대한민국", country, "10000")

        

@app.route('/exchange', methods=['GET', 'POST'])
def rate(): 
    main = []
    if request.method == 'POST':
        user_base = request.form.get('base', '').strip()
        user_currencies = request.form.get('currencies', '').strip()
        amount = request.form.get('amount', '').strip()
        exchange_result = exchange(user_base, user_currencies, amount)
    return render_template('main.html', mains=main)



@app.route('/weather', methods=['GET', 'POST'])
def weather():
    if request.method == 'POST':
        user_input_day = request.form.get('day', '').strip()
        user_input_country = request.form.get('country', '').strip() 
        weather_result = get_weather(user_input_country, user_input_day)
    return render_template("main.html", weather_resyuts=weather_result)

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)

    