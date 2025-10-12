import requests
import pandas as pd

# API URL
url = "https://www.airportal.go.kr/airport/searchAirport.do"

# 초기값
page_number = 1
page_size = 50  # 한 페이지당 가져올 데이터 수 (적절히 설정)
all_airports = []

while True:
    payload = {
        "pageNumber": page_number,
        "pageSize": page_size,
        "searchName": None
    }

    response = requests.post(url, json=payload)
    data = response.json()

    content = data.get("content", [])
    if not content:
        break  # 더 이상 데이터가 없으면 종료

    all_airports.extend(content)
    print(f"페이지 {page_number} 완료, 수집 데이터: {len(content)}개")

    page_number += 1

# 데이터프레임으로 변환
df = pd.DataFrame(all_airports)

# 필요한 컬럼만 추출
df = df[["name2", "iataCode", "icaoCode", "koCity", "city", "location", "homepage"]]

# CSV로 저장
df.to_csv("airport_list.csv", index=False, encoding="utf-8-sig")

print(f"총 공항 수집: {len(df)}개")
