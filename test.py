import requests, json

country = 'korea'
url = f'https://restcountries.com/v3.1/name/{country}'
req = requests.get(url)
print(req.status_code)  # 200이 나와야 정상
json_data = req.json()
print(json_data)

with open("countries.json", "w", encoding="utf-8") as f:
    json.dump((json_data), f, ensure_ascii=False, indent=4)

print("countries.json 파일이 생성되었습니다.")
