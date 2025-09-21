import requests
from flask import Flask, request, render_template
from Symbol import country_code_data_five_number
app = Flask(__name__)

api_key = "lfwWiH5cTMe8Foh-XJzH6g"

@app.route('/main', methods=['GET', 'POST'])
def weather():
    values = []
    data = []
    if request.method == 'POST':
        user_input_day = request.form.get('day', '').strip()
        user_STN = request.form.get('stn', '').strip()
        STN = [k for k, v in country_code_data_five_number.items() if v == user_STN]
        url = f"https://apihub.kma.go.kr/api/typ01/url/gts_syn1.php?tm={user_input_day}&dtm=3&stn=47&help=0&authKey={api_key}&stn={STN}"
        response = requests.get(url)
        text = response.text
        
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
                            data.append(parts[i])
                    values = [f"{a}: {b}" for a, b in zip(help, parts)]

                except ValueError:
                    continue    
    print("TA values:", values)
    return render_template("main.html", values=values)

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)