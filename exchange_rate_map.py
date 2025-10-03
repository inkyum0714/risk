import requests
from Symbol import symbol_data, country_code_data_three
from flask import Flask, request, render_template

app = Flask(__name__)

api_key = "fxr_live_0e9f7bba09e36d62b800cfea2147bdd6efaf"

@app.route('/main', methods=['GET', 'POST'])
def rate(): 
    main = []
    if request.method == 'POST':
        user_base = request.form.get('base', '').strip()
        user_currencies = request.form.get('currencies', '').strip()
        base = country_code_data_three[user_base]
        currencies = country_code_data_three[user_currencies]
        print(f"Base: {base}, Currencies: {currencies}")
        amount = request.form.get('amount', '').strip()

        url = f"https://api.fxratesapi.com/latest?amount={amount}&base={base}&currencies={currencies}&places=6&format=json&api_key={api_key}"

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
            main.append(printr_data)
            print(f"{printr_data}{symbol}")
        else:
            print(f"Error: {response.status_code}")
            
    return render_template('main.html', mains=main)

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)

    