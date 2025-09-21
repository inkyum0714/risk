import requests
from bs4 import BeautifulSoup

# 웹 페이지 요청
url = "https://www.iban.kr/currency-codes"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # 모든 <tr> 찾기
    rows = soup.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) >= 3:  # 최소 3개의 <td> 존재
            country = cols[0].text.strip()
            code = cols[2].text.strip()
            print(f"'{country}': '{code}'")
else:
    print(f"Error: {response.status_code}")
