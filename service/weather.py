from data.Symbol import country_code_data_five_number
from datetime import datetime, timedelta
import requests

WEATHER_API_KEY = "lfwWiH5cTMe8Foh-XJzH6g"

def get_weather(user_input_country, user_input_day):
    weather_result = []
    weather_data = []

    # 1. 입력값 처리
    user_input_day = user_input_day.replace("-", "")
    user_input_day_dt = datetime.strptime(user_input_day, "%Y%m%d")
    today = datetime.today()

    # 과거년도 보정
    if user_input_day_dt > today:
        user_input_day_dt = user_input_day_dt.replace(year=user_input_day_dt.year - 1)

    # 7일 범위 날짜 리스트
    date_list_datetime = [user_input_day_dt + timedelta(days=i) for i in range(-3, 4)]
    dates = [int(d.strftime("%Y%m%d")) for d in date_list_datetime]

    country = country_code_data_five_number[user_input_country]

    for day in dates:
        url = f"https://apihub.kma.go.kr/api/typ01/url/gts_syn1.php?tm={day}1200&dtm=2&stn=47&help=0&authKey={WEATHER_API_KEY}&stn={country}"
        response = requests.get(url)
        text = response.text

        start_idx = text.find("#START7777")
        end_idx = text.find("#7777END")
        if start_idx == -1 or end_idx == -1:
            continue

        data_block = text[start_idx + len("#START7777"):end_idx].strip()
        lines = [line for line in data_block.splitlines() if line.strip() and not line.startswith("#")]

        for line in lines:
            parts = line.split()
            if len(parts) >= 13:
                part = [int(float(parts[0])), int(float(parts[9])), int(float(parts[10])), int(float(parts[12]))]
                weather_data.append(part)

    if not weather_data:
        return ["데이터 없음"]

    labels = ["날짜", "WS : 풍속 (m/s)", "TA : 기온 (C)", "HM : 상대습도 (%)"]
    weather_values = []
    for col in range(1, 4): 
        col_values = [row[col] for row in weather_data if len(row) > col]
        avg = sum(col_values) / len(col_values) if col_values else 0
        weather_values.append(avg)

    weather_result = [f"{label}: {value:.1f}" for label, value in zip(labels[1:], weather_values)]

    temp = float(parts[10])       # 기온
    rh = float(parts[12])         # 상대습도
    discomfort_index = temp - 0.55 * (1 - rh/100) * (temp - 14.5)

    # 3) 결과에 추가
    weather_result.append(f"불쾌지수: {discomfort_index:.1f}")
    weather_result.insert(0, user_input_day)
    print(weather_result)
    return weather_result
