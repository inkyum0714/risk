from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# RapidAPI 헤더 직접 입력
HEADERS = {
    "x-rapidapi-key": "dd019e6396msh5b4c8d6763bb299p145742jsn20b7704bf7ae",
    "x-rapidapi-host": "visa-requirement.p.rapidapi.com",
    "Content-Type": "application/json"
}

@app.route('/main', methods=['GET', 'POST'])
def main():
    result = None
    error_msg = None

    if request.method == 'POST':
        passport = request.form.get('passport', '').strip().upper()
        destination = request.form.get('destination', '').strip().upper()

        if not passport or not destination:
            error_msg = "여권과 목적지 코드를 모두 입력하세요."
        else:
            url = "https://visa-requirement.p.rapidapi.com/v2/visa/check"
            payload = {"passport": passport, "destination": destination}

            try:
                response = requests.post(url, json=payload, headers=HEADERS)
                
                if response.status_code == 200:
                    data = response.json()
                    primary_rule = data.get("data", {}).get("visa_rules", {}).get("primary_rule", {})
                    visa_name = primary_rule.get("name", "정보 없음")
                    duration = primary_rule.get("duration", "")
                    result = f"{passport} 여권으로 {destination} 방문 시 비자: {visa_name} {duration}"
                elif response.status_code == 401:
                    error_msg = "인증 실패: API 키를 확인하세요."
                elif response.status_code == 403:
                    error_msg = "권한 없음: 무료 플랜 호출 한도를 초과했거나 접근이 제한되었습니다."
                elif response.status_code == 429:
                    error_msg = "API 호출 횟수 초과: 잠시 후 다시 시도하세요."
                else:
                    error_msg = f"HTTP 오류 {response.status_code}: {response.text}"

            except requests.exceptions.RequestException as e:
                error_msg = f"요청 오류: {e}"

    return render_template('main.html', result=result, error_msg=error_msg)

if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0', debug=True)
