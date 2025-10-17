from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
import json
import os
import time

# JSON 파일 경로 지정
json_path = os.path.join("data", "city_to_airport.json")

# JSON 파일 읽기
with open(json_path, "r", encoding="utf-8") as f:
    city_to_airport = json.load(f)

# 크롬 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # 창 안 보이게 (테스트 시엔 주석 처리 추천)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# 결과 저장용 딕셔너리
translated_data = {}
try_number = 0
try:
    for key, value in city_to_airport.items():
        try_number += 1
        # value를 번역하도록 수정
        encoded_text = quote(value)
        url = f"https://translate.google.co.kr/?sl=en&tl=ko&text={encoded_text}&op=translate"
        driver.get(url)

        # 번역 결과 기다리기
        try:
            wait = WebDriverWait(driver, 10)
            span = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ryNqvb")))
            top_text = span.text
        except Exception:
            top_text = ""
            print("⚠ 번역 실패:", value)
        print(try_number, f"{value} → {top_text}")

        translated_data[key] = top_text
        # 너무 빠르면 구글에서 차단할 수 있으므로 약간 대기
        time.sleep(1.5)

finally:
    driver.quit()

# 전체 결과를 JSON 파일로 저장
output_path = "translation_result.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=4)

print(f"\n✅ 전체 번역 결과가 '{output_path}' 파일로 저장되었습니다.")
