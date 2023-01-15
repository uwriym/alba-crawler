### 지역별 알바 정보를 크롤링하는 프로그램입니다.

url 및 스크랩 여부를 확인할 수 있는 지역번호.csv는 url/ 에 저장됩니다.  
스크랩 결과는 .json 형태로 저장되며 result/ 에 저장됩니다.  

지역번호.csv가 이미 존재한다면 해당 파일을 새로 만들 것인지(다시 url을 가져올 것인지)를 선택할 수 있습니다.  
지역번호.csv가 존재하지 않는다면 자동으로 url 스크랩부터 시작합니다.

---

에러 등의 이유로 프로그램 실행이 중단되었을 때, 스크랩이 진행된 url까지 csv의 scraped가 True로 변경되며,  
재실행 시 csv를 확인하여 scraped가 False인 url만 스크랩 진행합니다.

---
### 콘솔 출력 내용

- No.1 scrap failed(login required) -> 로그인을 필요로 하는 공고
- No.1 scraped successfully -> 스크랩 성공
- No.1 scrap failed(error) -> 스크랩 실패(에러 내용 확인 필요)
  - crawler.py의 line147, 160-161에 있는 예외 처리문을 제거하고 프로그램 재실행 시 에러 내용 확인 가능
- No.1 pass(scraped) -> 이미 스크랩되어 패스됨

