import requests
from Symbol import country_code_data_two
from flask import Flask, request, render_template

app = Flask(__name__)

api_key = "jiDRCL1%2FKFqcHeMt6Q8%2FwIFNhQoj79XSfFhNpfZCeNWBmGu8oDp%2B7P0gPHWcCr96h1YrqMtF2QGeyMItKFO%2FTA%3D%3D"

@app.route('/main', methods=['GET', 'POST'])
def rate():
    risk_data = None
    if request.method == 'POST':
        country_risk = request.form.get('riskmap', '').strip()
        country = country_code_data_two[country_risk]
        url = f"http://apis.data.go.kr/1262000/TravelAlarmService2/getTravelAlarmList2?serviceKey={api_key}&returnType=JSON&numOfRows=1&cond[country_iso_alp2::EQ]={country}"
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

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)