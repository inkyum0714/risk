from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
import json
import os
import time

json_path = os.path.join("data", "city_to_airport.json")

with open(json_path, "r", encoding="utf-8") as f:
    city_to_airport = json.load(f)

options = webdriver.ChromeOptions()
options.add_argument("--headless") 
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

translated_data = {}
try_number = 0
try:
    for key, value in city_to_airport.items():
        try_number += 1
        encoded_text = quote(value)
        url = f"https://translate.google.co.kr/?sl=en&tl=ko&text={encoded_text}&op=translate"
        driver.get(url)

        try:
            wait = WebDriverWait(driver, 10)
            span = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ryNqvb")))
            top_text = span.text
        except Exception:
            top_text = ""
            print("⚠ 번역 실패:", value)
        print(try_number, f"{value} → {top_text}")

        translated_data[key] = top_text
        time.sleep(0.5)

finally:
    driver.quit()
output_path = "translation_result.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(translated_data, f, ensure_ascii=False, indent=4)

print(f"\n✅ 전체 번역 결과가 '{output_path}' 파일로 저장되었습니다.")
