from selenium import webdriver
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import Counter
from webdriver_manager.chrome import ChromeDriverManager

import csv
import json

import os
from datetime import datetime
# from main import AREACODE


class UrlManager:

    def __init__(self, areacode):
        self.AREACODE = areacode

    def extract_url(self):

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        url = f"http://www.alba.co.kr/job/area/MainLocal.asp?viewtype=L&sidocd={self.AREACODE}&page=1"
        driver.get(url)

        last_page = driver.find_element(By.CSS_SELECTOR, "div.pagenation span.state").text.split("/")[1].strip()

        url_list = []

        # for i in range(int(last_page)): 나중에는 이걸로 사용
        for i in range(2):  # 일단은 2페이지까지만
            page = i + 1
            url = f"http://www.alba.co.kr/job/area/MainLocal.asp?viewtype=L&sidocd=031&page={page}"

            if page != 1:
                driver.get(url)

            top_alba = False
            try:
                driver.find_element(By.ID, "AreaTop")
                top_alba = True
            except:  # when TOP alba doesn't exist, keep "top_alba = False"
                pass

            if top_alba:  # when TOP alba exists
                top_urls = driver.find_elements(By.CSS_SELECTOR, "div#AreaTop tbody td.title > a:first-child")
                for url in top_urls:
                    url_list.append(url.get_attribute("href"))

            normal_urls = driver.find_elements(By.CSS_SELECTOR, "div#NormalInfo tbody td.title > a")
            for url in normal_urls:
                url_list.append(url.get_attribute("href"))

            print(f"page {page} url scraped")

        driver.quit()

        return url_list

    def save_url(self):
        url_list = self.extract_url()
        url_csv = open(f"{os.getcwd()}/url/{self.AREACODE}.csv", "w")
        writer = csv.writer(url_csv)

        writer.writerow(["index", "url", "scraped"])
        n = 1
        for url in url_list:
            writer.writerow([n, url, "False"])
            n += 1
        return

    # areacode_update.csv의 내용을 areacode.csv로 옮기는 함수
    def overwrite_url(self):
        try:
            updated_csv = open(f"{os.getcwd()}/url/{self.AREACODE}_update.csv", "r")
        except:
            return
        overwrite_csv = open(f"{os.getcwd()}/url/{self.AREACODE}.csv", "w")

        reader = csv.reader(updated_csv)

        url_dict = []

        n = 1
        for line in reader:
            if n != 1:
                url_dict.append({"index": line[0], "url": line[1], "scraped": line[2]})
            n += 1

        writer = csv.writer(overwrite_csv)
        writer.writerow(["index", "url", "scraped"])
        for i in url_dict:
            writer.writerow([i["index"], i["url"], i["scraped"]])
        return

    # load_url() 변수 바꿔서 위 함수에서 써도 될듯?

    def load_url(self):
        csv_for_scrap = open(f"{os.getcwd()}/url/{self.AREACODE}.csv", "r")
        reader = csv.reader(csv_for_scrap)

        url_dict = []

        n = 1
        for line in reader:
            if n != 1:
                url_dict.append({"index": line[0], "url": line[1], "scraped": line[2]})
            n += 1

        return url_dict

    def renew_url_status(self, url_dict):
        renewed_csv = open(f"{os.getcwd()}/url/{self.AREACODE}_update.csv", "w")

        writer = csv.writer(renewed_csv)
        writer.writerow(["index", "url", "scraped"])

        for i in url_dict:
            writer.writerow([i["index"], i["url"], i["scraped"]])
        return




