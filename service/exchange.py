from data.Symbol import country_code_data_three, symbol_data
import requests

EXCHANGE_API_KEY = "fxr_live_0e9f7bba09e36d62b800cfea2147bdd6efaf"

def exchange(user_base):
    print(user_base)
    base = country_code_data_three[user_base]
    print(f"Base: {base}")
    url = f"https://api.fxratesapi.com/latest?amount=1&base={base}&currencies=KRW&places=6&format=json&api_key={EXCHANGE_API_KEY}"
    print(url)
    symbol = None
    for currency in symbol_data:
        if currency["code"] == base:
            symbol = currency["symbol"]
            break

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        symbol = None
        for currency in symbol_data:
            if currency["code"] == 'KRW':
                symbol = currency["symbol"]
                break
        printr_data_1 = round(data['rates']['KRW'], 2)
        printr_data = f"{printr_data_1}{symbol}"
        printr_data
        print("환율 데이터 가져오기 성공:", printr_data)
        return printr_data