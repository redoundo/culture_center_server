# culture-center-project

### 프로젝트 소개

  	기업 소재의 문화 센터 뿐만 아니라 도서관 등에서 실행 되는 문화 강좌를 모아 제공합니다.
  	파편화 된 문화 강좌들을 쉽게 찾고 싶어서 진행한 프로젝트 입니다.
  	강좌 내용이 지속적으로 업데이트 되고 그에 맞는 크롤링이 필요하기 때문에 

---

### 주요 기능

    
---

### 문제 상황 및 해결 과정

1. 데이터를 수집하는 센터마다 강좌를 분류하는 기준이 상이하며 오분류 된 강좌가 존재 하는 상황.
   - 여러 사이트에서 크롤링을 해온 데이터를 재분류 해야 하는데 정규 분포식 만으로 해결 하는 게 힘들었습니다. 그래서 정규 표현식 대신 머신 러닝을 통해 데이터를 재분류를 하기로 결정 했습니다.
   - 미리 학습 시킨 모델을 파인 튜닝 하면 간단 하지만 제가 원하는 기준으로 텍스트 분류가 가능 하다는 걸 알게 되었습니다. 그렇게 크롤링한 강좌들을 제가 원하는 분류 기준으로 라벨링 한 뒤, kobert 모델을 사용해 학습시켰습니다.
   - 강좌 내용은 계속 달라지기 때문에 지속적인 학습이 필요 하겠으나, 정규 표현식으로 진행했을 때보다 정교한 분류가 가능해졌습니다.
   - [ml 레포지토리 참조](https://github.com/redoundo/culture_center_server/tree/ml)

2. 비슷한 과정을 거쳐 크롤링이 진행 되지만, 세부적인 내용은 다르기 때문에 크롤러가 크롤링 하는 사이트의 수만큼 존재 하여 관리하기 복잡한 상황.
     - 쿼리 스트링으로 검색 가능한 사이트와 아닌 사이트들을 나눠 추상화를 진행 했습니다.
         <details>
            <summary>쿼리 스트링 이용 가능한 크롤러의 추상 클래스</summary>
            <div>
               <pre>
                  <code>
                     class WithLinkCrawler: 
                         """
                         쿼리 스트링으로 검색 조건을 설정할 수 있는 사이트들을 대상으로 크롤링을 진행.
                         """
                         centerInfo: CenterInfoWithLink
                         page: Page  
                         total: int
                         pageCount: int
                         lectureHrefs: list[str]
                         lectureInfos: list[ClassIdInfos] 
                         def __init__(self, center_info: CenterInfoWithLink, page: Page) -> None:
                             self.page = page
                             self.centerInfo = center_info 
                             self.total = -1
                             self.pageCount = -1
                             self.lectureInfos = []
                             self.lectureHrefs = []
                             return 
                         def crawl(self): 
                              """
                              extract_lecture_info 를 제외한 메서드로 강의 들의 링크를 가져오는 역할을 한다.
                              extract_lecture_info 는 새로운 객체를 만들어 따로 진행.
                              :return:
                              """
                             pass 
                         def load_more(self): 
                              """
                              페이지네이션 처리
                              :return:
                              """
                             pass 
                         def get_loaded_lecture_url(self): 
                              """
                              로드된 강의들의 href를 가져 온다.
                              :return:
                              """
                             pass 
                         def extract_lecture_info(self, url: str, page: Page, info: dict): 
                              """
                              강의 정보를 가져 온다.
                              :param url:
                              :param page:
                              :param info:
                              :return:
                              """
                             pass 
                         def goto_page(self, url: str) -> None: 
                              """
                              url 페이지로 이동.
                              :param url: 지점, 대상, 카테고리가 세팅된 url
                              :return:
                              """
                             pass 
                         def rest_page(self):
                             pass 
                         def __call__(self, center_info: CenterInfoWithLink, page: Page):
                             self.__init__(center_info, page)
                             return
       </code>
       </pre>
       </div>
       </details>
        <details>
           <summary>쿼리 스트링 이용 불가능한 크롤러의 추상 클래스</summary>
           <pre> 
           <code>
           class NoLinkCrawler:
               """
               검색 조건이 쿼리스트링에 설정 되지 않아 크롤러가 검색 조건을 직접 설정 해야 하는 사이트들이 대상.
               """
               centerInfo: CenterInfoNoLink
               page: Page
               url: str
               total: int
               pageCount: int
               lectureHrefs: list[str]
               lectureInfos: list[ClassIdInfos]
                   def __init__(self, url: str, center_info: CenterInfoNoLink, page: Page) -> None:
                        self.centerInfo = center_info
                        self.page = page
                        self.url = url 
                        self.lectureInfos = []
                        self.lectureHrefs = []
                        self.pageCount = -1
                        self.total = -1
                        return
                  def crawl(self):
                        """
                        extract_lecture_info 를 제외한 메서드로 강의 들의 링크를 가져오는 역할을 한다.
                        extract_lecture_info 는 새로운 객체를 만들어 따로 진행.
                        :return:
                        """
                        pass
                  def search_option_setting(self) -> None:
                        """
                         크롤링을 하기 위해 target, category 설정 제외한 지역과 지점 설정만 한다.
                        :return:
                        """
                        pass
                  def load_more(self):
                         """
                         페이지네이션 처리
                         :return:
                         """
                         pass
                  def check_lecture_total(self):
                         """
                         설정한 조건으로 존재하는 강의가 있는지 확인. 있다면 self 멤버 변수의 수를 바꾸고 없으면 -1 상태로 냅둔다.
                         :return:
                         """
                         pass
                  def get_loaded_lecture_url(self):
                         """
                         로드된 강의들의 href 를 가져 온다.
                         :return:
                         """
                        pass
                  def extract_lecture_info(self, url: str, page: Page, info: dict):
                       """  
                       강의 href 를 통해 강의 정보를 가져 온다.
                       :param url: 내용을 추출할 url 
                       :param page: playwright Page 객체
                       :param info: url 을 가져 왔을 때의 context 
                       :return: 
                       """
                        pass
                  def __call__(self, url: str, center_info: CenterInfoNoLink, page: Page):
                        self.__init__(url, center_info, page)
                        return
       </code>
     </pre>  
   </details>
              
     - enum 클래스에 크롤러 자체의 클래스를 받는 대신 추상 클래스로 받게 만들어, 크롤러 객체 생성을 용이 하게 해주는 추상 팩토리 패턴을 구현 했습니다.
        <details>
            <summary>예시</summary>  
            <pre>
            <code>
                class NoLinkCrawlerFactory(enum.Enum):
                    """
                    쿼리 스트링 조합으로 검색이 불가능한 사이트들을 크롤링 하는 크롤러를 생산
                    """
                    HOMEPLUS = ("HOMEPLUS", HomePlusCrawler, "https://mschool.homeplus.co.kr/Lecture/Search",
                               "crawler/resource/homeplus.json")
                    EMART = ("EMART", EmartCrawler, "https://www.cultureclub.emart.com/enrolment",
                             "crawler/resource/emart.json")
                    LOTTEMART = ("LOTTEMART", LotteMartCrawler, "https://culture.lottemart.com/cu/gus/course/courseinfo/courselist.do?",
                                 "crawler/resource/lottemart.json")
                    AKPLAZA = ("AKPLAZA", AkplazaCrawler, "https://culture.akplaza.com/course/list02",
                               "crawler/resource/akplaza.json") 
                    def __init__(self, center: str, crawler: NoLinkCrawler, url: str, path: str):
                        """
                        크롤러에 필요한 내용과 크롤러를 가리키는 객체를 담는다.
                        :param center: 센터 이름
                        :param crawler: 센터의 크롤러
                        :param url: 센터 기본 url 주소
                        :param path: 센터 설정이 들어있는 파일의 주소
                        """
                        self.center = center
                        self.crawler = crawler
                        self.url = url
                        self.path = path
                        return
                    @classmethod
                    def get_crawler(cls, center: str) -> NoLinkCrawler:
                        """
                        사이트 이름으로 크롤러 클래스를 찾아 반환한다.
                        :param center: 사이트 이름
                        :return: 해당 사이트의 크롤러
                        """
                        return [member.crawler for name, member in cls.__members__.items() if name == center][0]
                    ....
           </code>
           </pre>
    </details>

    - 크롤러 클래스와 크롤러 클래스를 생성하는 과정이 분리되었기 때문에, 크롤러 클래스를 생성시키는 과정에서 변경사항이 존재 하더라도 크롤러에는 아무런 영향을 미치지 않아서 개발하기가 쉬워졌습니다.
3. 크롤링을 진행할 때 현재 어떤 상황인지 알기가 어려운 문제
    - dicord 알림을
      <details>
        <summary>discord 알림 전달 과정</summary>      
        <pre>
            if __name__ == '__main__':
                url_queue: queue.Queue = queue.Queue(maxsize=5)
                message_queue: queue.Queue = queue.Queue(maxsize=10) 
                messenger: DiscordMessenger = DiscordMessenger(message_queue=message_queue)
                url_thread: threading.Thread = threading.Thread(daemon=True, target=url_crawling, args=[url_queue, message_queue, ])
                info_thread: threading.Thread = threading.Thread(daemon=True, target=info_crawling, args=[url_queue, message_queue, ])
                message_thread: threading.Thread = threading.Thread(daemon=True, target=messenger.send_message)
                url_thread.start()
                info_thread.start() 
                url_thread.join()
                info_thread.join()
                database.create_train_sample(queue=message_queue)
                database.connection.close() 
                message_thread.join() 
      </pre>
</details>

4. 전역 에러 처리
    - flask app 에 error handler 를 등록하여 개별적으로 에러를 처리 하지 않고 한곳에서 에러를 처리하게끔 구성 했습니다.
        <details>
            <summary>error handler 등록 코드</summary>
            <pre>
                def global_error_handler(app: Flask):
                    """
                    flask application 에 사용자 정의된 예외를 포함한 httpException 을 다룰 수 있는 처리자를 미리 등록 해놓음.
                    :param app: flask application
                    :return: app
                    """
                    def error_handler(error):
                        if isinstance(error, CustomException):
                            res: dict = {
                                "errorName": error.errorName,
                                "status": error.status,
                                "message": error.message
                            }
                        elif isinstance(error, HTTPException):
                            res: dict = {
                                "errorName": error.name,
                                "status": error.code,
                                "message": error.description
                            }
                        else:
                            message = _aborter.mapping[400].description
                            res: dict = {
                                "errorName": "ELSE_ERROR",
                                "status": 400,
                                "message": message
                            }
                        response = jsonify(res)
                        response.status_code = res["status"]
                        return response 
                    for http in list(default_exceptions.values()):
                        app.register_error_handler(http, error_handler)
                    app.register_error_handler(CustomException, error_handler)
                    return app 
            </pre>
        </details>

    - 
### 아키텍쳐
![culture-center](https://github.com/redoundo/culture_center_server/assets/96558064/60d9da7a-812b-4580-8b3c-e0af6cfe1c57)

### 웹사이트 기능
[웹 사이트 기능 코드](https://github.com/redoundo/culture_center_server/blob/b7571b0cb546c174601769b02ff591dd49fafc90/app.py)
1. 강좌 검색
    <details>
        <summary>강좌 검색 과정</summary>
        <img src="https://github.com/redoundo/culture_center_server/assets/96558064/b877dea5-d4e3-4b82-bb55-559c69a54372">
   </details>
    <details>
        <summary>검색 영상</summary>
            <img src="https://github.com/redoundo/culture_center_server/assets/96558064/3adb735a-a8c9-4201-94ff-479100c47088"/>
    </details>
2. 강좌 찜하기 및 지원하기
   <details>
        <summary>강좌 찜하기 및 지원 과정</summary>
        <img src="https://github.com/redoundo/culture_center_server/assets/96558064/bbef43c0-886a-4fb5-98b2-fcd7e4f93c0a">
   </details>
   <details>
        <summary>찜한/ 지원한 강좌 삭제 과정</summary>
        <img src="https://github.com/redoundo/culture_center_server/assets/96558064/9792e4f4-1750-4bc7-8b57-ef2fa3eddd22">
   </details>
    <details>
        <summary>강의 찜한 / 지원한 강좌 삭제 영상</summary>
        <img src="https://github.com/redoundo/culture_center_server/assets/96558064/cb0a7134-7098-4e33-9480-96f6ea350dfd"/>
    </details>

3. sns 로그인
    <details>
        <summary>sns 로그인 과정</summary>
        <img src="https://github.com/redoundo/culture_center_server/assets/96558064/970d395c-b6ff-4a18-a392-ab2239fc4346">
   </details>
    <details>
        <summary>회원정보 변경 및 탈퇴 영상</summary>
        <img src="https://github.com/redoundo/culture_center_server/assets/96558064/9d5c2a63-9c8c-4b78-a375-87049c8a4a98"/>
    </details>



### Api 레퍼런스

[postman api](https://documenter.getpostman.com/view/25808797/2sA3JRZebp)

### 트러블 슈팅 

<details >
    <summary>windows os 인 ec2 인스턴스에서 ubuntu 이미지 사용시 에러 발생</summary>
    <div style="padding: 15px;font-style: italic">
        latest: Pulling from library/ubuntu 2024-05-23 03:16:56 [stderr]no matching manifest for windows/amd64 10.0.20348 in the manifest list entries
    </div>
    <div style="padding: 9px">
        windows os 에 설치된 docker 에서는 linux 계열 이미지를 사용하지 못하기 때문에 발생하는 에러 입니다.
wsl을 통해 linux 계열 이미지를 사용할 수는 있으나 wsl 과 ubuntu를 설치해본 결과 인스턴스의 심각한 용량 부족으로 인해 새로운 ec2 인스턴스를 생성하기로 결정했습니다.
    </div>
</details> 


### 사용 기술

`front-end`
- React
- Recoil
- Vercel
  

`back-end`

- Flask
- Gunicorn
- Nginx
- SQLAlchemy
- Docker

`deploy`
- Github Actions
- AWS S3
- AWS CodeDeploy
- AWS EC2

`crawler` 
- Playwright

`database`
- Mysql
- AWS RDS


## ERD

![](C:\Users\admin\Downloads\culture_center_erm.png)
