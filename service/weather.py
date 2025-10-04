from data.Symbol import country_code_data_five_number
import requests

WEATHER_API_KEY = "lfwWiH5cTMe8Foh-XJzH6g"

def get_weather(user_input_country, user_input_day):
        weather_result = []
        weather_data = []
        country = country_code_data_five_number[user_input_country]
        url = f"https://apihub.kma.go.kr/api/typ01/url/gts_syn1.php?tm={user_input_day}&dtm=3&stn=47&help=0&authKey={WEATHER_API_KEY}&stn={country}"
        response = requests.get(url)
        text = response.text
        print(country)
        start_idx = text.find("#START7777")
        end_idx = text.find("#7777END")
        if start_idx != -1 and end_idx != -1:
            data_block = text[start_idx + len("#START7777"):end_idx].strip()
            lines = data_block.splitlines()

            for line in lines:
                if line.strip() == "" or line.startswith("#"):
                    continue
                parts = line.split()
                help = ["날짜",
                        "국가 지명번호",
                        "IW : 풍속단위",
                        "IR : 강수자료 유무",
                        "VV : 시정",
                        "WD : 풍향",
                        "WS : 풍속 (m/s)",
                        "TA : 기온 (C)" ,
                        "HM : 상대습도 (%)" ,]

                try:
                    for i in range(10):
                        if parts[i] != "-99.0" and parts[i] != "-999":
                            weather_data.append(parts[i])
                    weather_result = [f"{a}: {b}" for a, b in zip(help, parts)]

                except ValueError:
                    continue  

                print("TA values:", weather_result)

                return weather_result