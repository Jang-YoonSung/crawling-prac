from selenium import webdriver as wb
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

def crawling(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)).strftime("%Y%m%d") for i in range((end-start).days+1)]

    print(dates)
    for i in range(len(dates)):
        if (datetime.strptime(dates[i], "%Y%m%d").weekday() <5) : 
            print("평일")
        else:
            print("주말")


    driver = wb.Chrome()
    driver.get("https://broadcast.tvchosun.com/news/newspan/ch19.cstv")  # 웹사이트 URL 입력
    driver.implicitly_wait(10)

    # 1. calendar-picker가 안 보이는 경우 on으로 바꾸기
    calendar = driver.find_element(By.CLASS_NAME, "calendar-picker")
    driver.execute_script("arguments[0].classList.add('on');", calendar)  # on 상태로 변경

    time.sleep(1)  # 상태 변경 후 대기

    target_year = "2024년"
    year_element = driver.find_element(By.XPATH, f"//ul[@class='year-list']//a[text()='{target_year}']")
    driver.execute_script("arguments[0].click();", year_element)

    target_month = "2월"
    month_element = driver.find_element(By.XPATH, f"//ul[@class='month-list']//a[text()='{target_month}']")
    driver.execute_script("arguments[0].click();", month_element)

    target_date = "1"
    date_element = driver.find_element(By.XPATH, f"//ul[@class='date-list']//a[text()='{target_date}']")
    driver.execute_script("arguments[0].click();", date_element)

    driver.execute_script("arguments[0].setAttribute('class', arguments[0].getAttribute('class').replace('on', ''))", calendar)

    time.sleep(1)  # 변경 적용을 위해 대기

    links = [a.get_attribute("href") for a in driver.find_elements(By.CSS_SELECTOR, "ul.item-list li a")]
    print(links)
    
    for url in links:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find_all('div', "text-box")
        print(content)


    driver.quit()

crawling("2025-01-17", "2025-01-23")