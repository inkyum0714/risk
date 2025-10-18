from data.Symbol import country_code_data_five_number
from datetime import datetime, timedelta
import requests

WEATHER_API_KEY = "lfwWiH5cTMe8Foh-XJzH6g"

def get_weather(user_input_city, user_input_day):
    weather_result = []
    weather_data = []
    print(user_input_city)
    user_input_day = user_input_day.replace("-", "")
    user_input_day_dt = datetime.strptime(user_input_day, "%Y%m%d")
    today = datetime.today()

    if user_input_day_dt > today:
        user_input_day_dt = user_input_day_dt.replace(year=user_input_day_dt.year - 1)

    date_list_datetime = [user_input_day_dt + timedelta(days=i) for i in range(-3, 4)]
    dates = [int(d.strftime("%Y%m%d")) for d in date_list_datetime]

    country = country_code_data_five_number[user_input_city]

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
        print("데이터 없음")
        return ["데이터 없음"]


    temp = float(parts[10])       # 기온
    rh = float(parts[12])         # 상대습도
    discomfort_index = temp - 0.55 * (1 - rh/100) * (temp - 14.5)

    # 3) 결과에 추가
    weather_result = f"불쾌지수: {discomfort_index:.1f}"
    return weather_result
