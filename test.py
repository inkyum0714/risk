from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://data.kma.go.kr/tmeta/stn/selectStnList.do")

# 모든 div#sidetree 가져오기
sidetree_divs = driver.find_elements(By.ID, "sidetree")

# 두 번째 요소 선택
sidetree_div = sidetree_divs[0]

# 첫 번째 ul 가져오기
first_ul = sidetree_div.find_element(By.TAG_NAME, "ul")

# 첫 번째 li 가져오기
first_li = first_ul.find_element(By.TAG_NAME, "li")

first_ul_1 = first_li.find_element(By.TAG_NAME, "ui")


print(first_ul_1.get_attribute("outerHTML"))

driver.quit()
