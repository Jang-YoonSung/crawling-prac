from selenium import webdriver as wb
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta
import re

import requests
from bs4 import BeautifulSoup

def crawling(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]

    removeList = ["\n", "\t", "\r", '·', '...', '“', '”', '‘', '’', '(', ')', 'ㆍ', '…', ',', '-', '▶', '\'', '"', 
        'EPA', '=', '연합뉴스', '로이터', 'AP', '※', '☎', '>', '기자', '앵커', '[앵커]', '[리포트]', 'Q.', 'A.', '.', '!', '? ', 
        '(영상취재 :', '(영상편집 :', '[날씨]', ' : ', ']', '[', "/", ":",
        "1.","2.","3.","4.","5.","6.","7.","8.","9."]
    pattern = "|".join(map(re.escape, removeList))

    driver = wb.Chrome()
    driver.get("https://broadcast.tvchosun.com/news/newspan/ch19.cstv")  # 웹사이트 URL 입력
    driver.implicitly_wait(10)

    resultContent=[]
    for i in range(len(dates)):
        if datetime.strptime(dates[i], "%Y%m%d").weekday() < 5 :    
            # 1. calendar-picker가 안 보이는 경우 on으로 바꾸기
            calendar = driver.find_element(By.CLASS_NAME, "calendar-picker")
            driver.execute_script("arguments[0].classList.add('on');", calendar)  # on 상태로 변경

            time.sleep(1)  # 상태 변경 후 대기

            target_year = dates[i][:4] + "년"
            year_element = driver.find_element(By.XPATH, f"//ul[@class='year-list']//a[text()='{target_year}']")
            driver.execute_script("arguments[0].click();", year_element)

            target_month = dates[i][4:6] + "월"
            if target_month[0] == '0':
                target_month = target_month[1:]
            month_element = driver.find_element(By.XPATH, f"//ul[@class='month-list']//a[text()='{target_month}']")
            driver.execute_script("arguments[0].click();", month_element)

            target_date = dates[i][6:]
            if target_date[0] == '0':
                target_date = target_date[1:]
            date_element = driver.find_element(By.XPATH, f"//ul[@class='date-list']//a[text()='{target_date}']")
            driver.execute_script("arguments[0].click();", date_element)

            driver.execute_script("arguments[0].setAttribute('class', arguments[0].getAttribute('class').replace('on', ''))", calendar)

            time.sleep(1)  # 변경 적용을 위해 대기

            links = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "ul.item-list li a")]
            
            for url in links:
                response = requests.get(url)
                html = response.text
                soup = BeautifulSoup(html, 'html.parser')
                content = soup.find_all('div', "text-box") #div 태그의 text-box class를 찾아 반환

                for text in content:
                    clean_text = re.sub(pattern, "", text.get_text().strip())
                    print(clean_text)

                    resultContent.append(clean_text) #텍스트만 추출, html 태그는 제거
    driver.quit()
    return resultContent

result = crawling("2025-01-17", "2025-01-30")

file_name = './output_doc_20250131.txt'

with open(file_name, 'w', encoding='UTF-8') as f:
    f.write('\n'.join(result))