import url_manager
import crawler

import os

import json
from _datetime import datetime
now = datetime.now()


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

## 해야할 것

# json으로 결과물 저장하면 시간에 따라 저장되기 때문에 기존에 스크랩되었던 내용은 제외되고 그 다음 것부터 저장됨
# -> 기존 것과 merge하는 함수 만들 필요 있음(최종 json 파일 return)

# 전체 과정 쭉 훑을 필요 있음

# province 필요한가?


# 지역번호
AREACODE = "031"

um = url_manager.UrlManager(AREACODE)
cr = crawler.AlbaCrawler()

while True:
    ans = input("Want to rescrap url? (y/n)")
    if ans == "y" or ans == "Y":
        um.save_url()  # AREACODE.csv 생성
        break
    if ans == "n" or ans == "N":
        break

    print("Put the right answer.")


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


# 데이터 뽑을 url 리스트를 AREACODE.csv로부터 가져오기
url_dict_list = um.load_url()
'''
# 임시 url 데이터
url_dict_list = [{"index": "1",
                  "url": "http://www.alba.co.kr/job/Detail.asp?adid=119562979&listmenucd=LOCAL",
                  "scraped": "False"},
                 {"index": "2",
                  "url": "http://www.alba.co.kr/job/Detail.asp?adid=119603034&listmenucd=LOCAL",
                  "scraped": "False"}
                 ]
'''

# 첫 번째 돌릴 때는 그냥 json 생성
# 두 번째 돌릴 때는 원래 json과 새로 만들어진 json을 합쳐서 json 생성 (파일 수 2개)
# 세 번째 돌릴 때는 (파일 수 3개_
# 이런 식인데 결국 맨 마지막 파일이 모든 알바의 정보를 담고 있는 json이 되는 것


def manage_extract():
    result_list = []
    n = 1
    for i in url_dict_list:

        if i["scraped"] == "False":
            # try:
                result_json = cr.extract_data(i["url"], driver)
                if result_json == "login required":
                    i["scraped"] = "login required"
                    print(f"No.{n} url requires login")
                else:
                    result_list.append(result_json)
                    # scrap된 url의 scraped를 True로 변환
                    i["scraped"] = "True"
                    print(f"No.{n} is being scraped")
            # except:
                # print(f"No.{n} is not scraped")

        elif i["scraped"] == "login required":
            print(f"No.{n} requires login")

        else:
            print(f"No.{n} url was scraped")

        n += 1

        if n == 16:
            break

    driver.quit()

    json_list = []
    dir_path = f"{os.getcwd()}/result"
    for (root, directories, files) in os.walk(dir_path):
        for file in files:
            if '.json' in file:
                file_path = os.path.join(root, file)
                json_list.append(file_path)

    if len(json_list) > 0:
        latest_json_path = json_list[-1]
        with open(latest_json_path) as latest:
            latest_data = json.load(latest)

        with open(f"result/{AREACODE}_{now.strftime('%Y-%m-%d %H:%M:%S')}.json", "w", encoding="utf-8") as json_file:
            json.dump(latest_data+result_list, json_file, indent='\t', ensure_ascii=False)
    else:
        with open(f"result/{AREACODE}_{now.strftime('%Y-%m-%d %H:%M:%S')}.json", "w", encoding="utf-8") as json_file:
            json.dump(result_list, json_file, indent='\t', ensure_ascii=False)

    return url_dict_list

um.renew_url_status(manage_extract())


um.overwrite_url()








