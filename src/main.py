import os

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import url_csv_manager
import crawler

try:
    os.chdir('src/..')
except:
    os.chdir('../')

# 지역번호
## 서울(02), 경기(031), 인천(032), 대전(042), 대구(053), 부산(051), 울산(052), 광주(062), 제주(064)
## 강원(033), 세종(044), 충북(043), 충남(041), 경북(054), 경남(055), 전북(063), 전남(061), 전국(99)
print("서울(02), 경기(031), 인천(032), 대전(042), 대구(053), 부산(051), 울산(052), 광주(062), 제주(064)\n강원(033), 세종(044), 충북(043), 충남(041), 경북(054), 경남(055), 전북(063), 전남(061), 전국(99)")
AREACODE = input("AREACODE: ")  # 검색하고자 하는 지역의 지역번호 설정


um = url_csv_manager.UrlManager(AREACODE)
cr = crawler.AlbaCrawler(AREACODE)

while True:
    csv_list = []
    csv_list_areacode = []

    dir_path = f"{os.getcwd()}/url"
    for (root, directories, files) in os.walk(dir_path):
        for file in files:
            if '.csv' in file:
                file_path = os.path.join(root, file)
                csv_list.append(file_path)

    for c in csv_list:
        if AREACODE == c[-7:-4] or AREACODE == c[-6:-4]:
            csv_list_areacode.append(c)

    if len(csv_list_areacode) != 0:
        print(f"이미 지역번호가 {AREACODE}인 URL 리스트가 존재합니다. URL을 다시 수집할까요? \n재수집 시 result 디렉토리에 있는 지역번호가 {AREACODE}인 json 파일은 모두 삭제됩니다.")
        ans = input("(y/n)")
        if ans == "y" or ans == "Y":
            um.save_url(True)  # AREACODE.csv 재생성
            break
        if ans == "n" or ans == "N":
            break
        print("Put the right answer.")

    else:
        um.save_url(False)  # AREACODE.csv 최초생성
        break


url_dict_list = um.load_url()

num_of_item = int(input(f"How many alba info? (max: {len(url_dict_list)}) : "))

# Chrome Browser Driver Setting
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

while True:
    if num_of_item > len(url_dict_list):
        print("Please enter a number less than max.")
    else:
        url_list_to_save = cr.manage_extract(driver, url_dict_list, num_of_item)
        break

um.update_url_status(url_list_to_save)

um.overwrite_url()
