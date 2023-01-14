import time

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


class AlbaCrawler:

    def __init__(self):
        return

    def load_url(self):
        url_dict = []
        url_file = open(f"{os.getcwd()}/url.csv", "r")
        reader = csv.reader(url_file)

        for line in reader:
            url_dict.append({"url": line[0], "scraped": line[1]})

        return url_dict

    def renew_url_csv(self):
        return

    def extract_data(self, url, driver):

        driver.get(url)

        login_required = True
        try:
            alert = driver.switch_to.alert
            alert.dismiss()
        except:
            login_required = False

        if login_required:
            return "login required"


        title = driver.find_element(By.CSS_SELECTOR, "h2.detail-content__title").text
        company = driver.find_element(By.CSS_SELECTOR, "strong.detail-content__tag-branch").text
        post_date = driver.find_element(By.CSS_SELECTOR, "div#DetailView div.detail-regist__date > em:first-child").text

        # 지역 필터

        n = 3
        while True:
            dl = driver.find_element(By.CSS_SELECTOR, f"div#InfoWork dl:nth-child({n})").text
            address = driver.find_element(By.CSS_SELECTOR, f"div#InfoWork dl:nth-child({n-1})").text.replace("근무지주소", "").strip()
            if "동정보" in dl:
                break
            else:
                n += 1


        raw_local_info = dl.replace("동정보", "").strip()
        local_info = raw_local_info.split(" ")
        province = local_info[0].strip()
        city = local_info[1].strip()
        dong = local_info[2].strip()

        # 모집조건
        sex = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:first-child > dl:nth-child(2) > dd").text
        age = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:first-child > dl:nth-child(3) > dd").text.replace('\n',' / ')
        education = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:first-child > dl:nth-child(4) > dd").text
        occupation = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:first-child > dl:nth-child(5) li").text
        jop_type = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:first-child > dl:nth-child(6) > dd").text
        num_of_recruits = driver.find_element(By.CSS_SELECTOR,
                                            "div.detail-content__condition-list:first-child > dl:nth-child(7) > dd").text
        try:
            prefer_treat = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:first-child > dl:nth-child(8) > dd").text
        except:
            prefer_treat = "X"

        pay_type = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:nth-child(2) > dl:nth-child(2) > dd > p > i").text.strip()
        pay_money = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:nth-child(2) > dl:nth-child(2) > dd > p > strong").text+"원".strip()
        emp_period = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:nth-child(2) > dl:nth-child(3) > dd").text
        working_day = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:nth-child(2) > dl:nth-child(4) > dd").text
        working_time = driver.find_element(By.CSS_SELECTOR, "div.detail-content__condition-list:nth-child(2) > dl:nth-child(5)").text.replace("근무시간", "").strip().replace("\n", " / ")


        result_json = {
            "title": title,
            "company": company,
            "address": address,
            "province": province, # 필요한가?
            "city": city,
            "dong": dong,
            "postDate": post_date,
            "sex": sex,
            "age": age,
            "education": education,
            "occupation": occupation,
            "jobType": jop_type,
            "numberOfRecruits": num_of_recruits,
            "preferential": prefer_treat,
            "payType": pay_type,
            "payMoney": pay_money,
            "employmentPeriod": emp_period,
            "workingDay": working_day,
            "workingTime": working_time,
            "url": url
        }

        return result_json

