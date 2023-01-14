import url_csv_manager
import crawler

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


# 지역번호
## 서울(02), 경기(031), 인천(032), 대전(042), 대구(053), 부산(051), 울산(052), 광주(062), 제주(064)
## 강원(033), 세종(044), 충북(043), 충남(041), 경북(054), 경남(055), 전북(063), 전남(061), 전국(99)
AREACODE = "033"

# Create Instance
um = url_csv_manager.UrlManager(AREACODE)
cr = crawler.AlbaCrawler(AREACODE)

while True:
    ans = input("Want to rescrap url? (y/n)")
    if ans == "y" or ans == "Y":
        um.save_url()  # AREACODE.csv 생성
        break
    if ans == "n" or ans == "N":
        break
    print("Put the right answer.")

# Chrome Browser Driver Setting
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


url_dict_list = um.load_url()

url_list_to_save = cr.manage_extract(driver, url_dict_list)

um.update_url_status(url_list_to_save)

um.overwrite_url()