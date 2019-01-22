import time
import requests
import lxml.html
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By #https://www.seleniumhq.org/docs/03_webdriver.jsp#locating-ui-elements-webelements
import csv

#검색 page가 로딩 되는 시간을 대기하기 위한 모듈
from selenium.webdriver.support.ui import WebDriverWait

# 예외 처리를 위한 모듈
from selenium.webdriver.support import expected_conditions as EC

main_url = "https://news.naver.com/main/ranking/popularDay.nhn"

driver = webdriver.Chrome("C:/driver/chromedriver.exe")
driver.get(main_url)
time.sleep(3)
driver.implicitly_wait(10) # seconds

def scraping():
        article_list = driver.find_elements_by_css_selector(".ranking_category_item a")
        article_urls = [item.get_attribute('href') for item in article_list]
        for article in article_urls:
                try:
                        driver.get(article)
                        soup = BeautifulSoup(driver.page_source, "html.parser")
                        headlines = soup.select('.ranking_headline a')
                        for headline in headlines:
                                # print(headline.text)
                                results.append(headline.text)
                except:
                        pass

def save():
        with open('day_one.csv', 'w', encoding = 'utf-8') as f:
                csv_writer = csv.writer(f)
                for result in results:
                        csv_writer.writerow(result)

# 1. crawling 하는 시점의 날짜 headlines
results = []
day_one = driver.find_element_by_xpath('//*[@id="wrap"]/table/tbody/tr/td[2]/div/div[12]/a[1]')
day_one_url = day_one.get_attribute('href')
scraping()

for i in range(8):
    driver.back()

# 2. crawling 하는 시점의 하루 전 날짜 headlines
day_two = driver.find_element_by_xpath('//*[@id="wrap"]/table/tbody/tr/td[2]/div/div[12]/a[1]')
day_two_url = day_two.get_attribute('href')
day_two.click()
scraping()

save()

time.sleep(3)
driver.close()

    
    
        