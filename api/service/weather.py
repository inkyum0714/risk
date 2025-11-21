from datetime import datetime, timedelta
import requests, json, os

WEATHER_API_KEY = "lfwWiH5cTMe8Foh-XJzH6g"

def get_weather(user_input_city, user_input_day):
    current_dir = os.path.dirname(__file__)  

    weather_file_path = os.path.join(current_dir, "weather_data.json")
    weather_file_path = os.path.abspath(weather_file_path)

    if not os.path.exists(weather_file_path):
        data = {}
    else:
        try:
            with open(weather_file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                data = json.loads(content) if content else {}
        except json.JSONDecodeError:
            data = {}

    country_code_path = os.path.join(current_dir, "..", "data", "country_code_data_five.json")
    country_code_path = os.path.abspath(country_code_path)

    with open(country_code_path, "r", encoding="utf-8") as f:
        country_code_data_five_number = json.load(f)
    weather_result = [] 
    weather_data = []
    user_input_day = user_input_day.replace("-", "")
    user_input_day_dt = datetime.strptime(user_input_day, "%Y%m%d")
    today = datetime.today()
    flag = False
    if user_input_day_dt > today:
        user_input_day_dt = user_input_day_dt.replace(year=user_input_day_dt.year - 1)

    date_list_datetime = [user_input_day_dt + timedelta(days=i) for i in range(-3, 4)]
    dates = [int(d.strftime("%Y%m%d")) for d in date_list_datetime]
    country = country_code_data_five_number[user_input_city]
    try:
        for day in dates:
            str_day = str(day)
            flag = False
            for i in range(len(data.get(user_input_city, []))):
                if str(data[user_input_city][i]["날짜"])[:8] == str_day:
                    print("최적화")
                    weather_data.append(data[user_input_city][i])
                    temp = data[user_input_city][i]["기온"]
                    rh = data[user_input_city][i]["상대습도"]
                    discomfort_index = discomfort_index = temp - 0.55 * (1 - rh/100) * (temp - 14.5)
                    weather_result.append(round(discomfort_index, 1))
                    flag =True
                    break
            if flag == True:
                continue

            url = f"https://apihub.kma.go.kr/api/typ01/url/gts_syn1.php?tm={day}1200&dtm=2&stn=47&help=0&authKey={WEATHER_API_KEY}&stn={country}" 
            print(url)
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
                    date = int(float(parts[0]))
                    wind = int(float(parts[9]))
                    temp = int(float(parts[10]))
                    rh = int(float(parts[12]))

                    weather_data.append([date, wind, temp, rh])
                    discomfort_index = float(parts[10]) - 0.55 * (1 - float(parts[12])/100) * (float(parts[10]) - 14.5)
                    weather_result.append(round(discomfort_index, 1))

                    if user_input_city not in data or not isinstance(data[user_input_city], list):
                        data[user_input_city] = []

                    if not any(record["날짜"] == date for record in data[user_input_city]):
                        data[user_input_city].append({
                            "날짜": date,
                            "풍속": wind,
                            "기온": temp,
                            "상대습도": rh,
                            "총합": [date, wind, temp, rh]
                        })
        print(weather_data)
        if not weather_data:
            return ["데이터 없음"]
    except TimeoutError as e:
        print("기상청 서버 문제")

    return weather_result, weather_data 