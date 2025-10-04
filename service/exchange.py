from data.Symbol import country_code_data_three, symbol_data
import requests

def exchange(user_base, user_currencies, amount):
    EXCHANGE_API_KEY = "fxr_live_0e9f7bba09e36d62b800cfea2147bdd6efaf"
    base = country_code_data_three[user_base]
    currencies = country_code_data_three[user_currencies]
    print(f"Base: {base}, Currencies: {currencies}")
    exchange_result = []
    url = f"https://api.fxratesapi.com/latest?amount={amount}&base={base}&currencies={currencies}&places=6&format=json&api_key={EXCHANGE_API_KEY}"

    symbol = None
    for currency in symbol_data:
        if currency["code"] == currencies:
            symbol = currency["symbol"]
            break

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        symbol = None
        for currency in symbol_data:
            if currency["code"] == currencies:
                symbol = currency["symbol"]
                break
        printr_data_1 = round(data['rates'][currencies], 2)
        printr_data = f"{printr_data_1}{symbol}"
        exchange_result.append(printr_data)
        return exchange_result