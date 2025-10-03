from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, re, json

driver = webdriver.Chrome()
driver.get("https://data.kma.go.kr/tmeta/stn/selectStnList.do")

# 1. 지정한 XPath 클릭
first_link = WebDriverWait(driver, 120).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/div/div[2]/div[3]/div[3]/div[2]/form/div[2]/div[1]/div/div/div/div/ul/li/ul/li[6]/a[1]"))
)

# 스크롤 후 자바스크립트 클릭
driver.execute_script("arguments[0].scrollIntoView(true);", first_link)
driver.execute_script("arguments[0].click();", first_link)

# 2. 내부 자식 label 중 "GTS기상" 포함된 label 클릭
# first_link의 부모에서 상대 XPath로 찾음
gts_label = WebDriverWait(driver, 202).until(
    EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'GTS기상')]"))
)
gts_label.click()

# 3. 10초 대기
time.sleep(10)

# 4. 페이지 전체에서 두 번째 div#sidetree 가져오기
second_sidetree = WebDriverWait(driver, 220).until(
    lambda d: d.find_elements(By.ID, "sidetree")[1] if len(d.find_elements(By.ID, "sidetree")) >= 2 else False
)

# 5. 내용 출력
print(second_sidetree.get_attribute("outerHTML"))
# second_sidetree 내부에서 for 속성이 ztree로 시작하는 label 찾기
labels = second_sidetree.find_elements(By.XPATH, ".//label[starts-with(@for, 'ztree')]")

# 각 label 출력
all_result = {}  # 초기화

for label in labels:
    la = label.get_attribute("outerHTML")
    print(la)  # 디버깅용
    matches = re.findall(r'>(.*?) \((\d+)\)<', la)
    if matches:
        all_result.update({name: int(code) for name, code in matches})

with open("countries.json", "w", encoding="utf-8") as f:
    json.dump(all_result, f, ensure_ascii=False, indent=4)

print("countries.json 파일이 생성되었습니다.")

    
