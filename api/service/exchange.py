import requests, os, json

EXCHANGE_API_KEY = "fxr_live_0e9f7bba09e36d62b800cfea2147bdd6efaf"

def exchange(user_base):
    current_dir = os.path.dirname(__file__)
    country_code_data_three_path = os.path.join(current_dir, "..", "data", "country_code_data_three.json")
    with open(country_code_data_three_path, "r", encoding="utf-8") as f:
        country_code_data_three_number = json.load(f) 

    json_path_symbol = os.path.join(current_dir, "..", "data", "symbol.json")
    with open(json_path_symbol, "r", encoding="utf-8") as f:
        symbol_data = json.load(f)

    base = country_code_data_three_number[user_base]
    url = f"https://api.fxratesapi.com/latest?amount=1&base={base}&currencies=KRW&places=6&format=json&api_key={EXCHANGE_API_KEY}"
    symbol = None
    for currency in symbol_data:
        if currency["code"] == base:
            symbol = currency["symbol"]
            print(symbol)
            break
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        for currency in symbol_data:
            if currency["code"] == 'KRW':
                symbol_KRW = currency["symbol"]
                break
        printr_data_1 = round(data['rates']['KRW'], 2)
        printr_data = f"{printr_data_1}{symbol_KRW}"
        print("환율 데이터 가져오기 성공: 1", symbol , printr_data)
        return [printr_data, symbol]