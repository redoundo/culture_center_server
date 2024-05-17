# culture-center-project

### 프로젝트 소개

  	기업 소재의 문화 센터 뿐만 아니라 도서관 등에서 실행 되는 문화 강좌를 모아 제공합니다.
  	파편화 된 문화 강좌들을 쉽게 찾고 싶어서 진행한 프로젝트 입니다.
---

### 프로젝트 특징

  	지원한 강좌가 진행 되는 날짜마다 사용자에게  firebase 클라우드 메시징을 이용해 강좌 알림을 보내줍니다.
---

### 문제 상황 및 해결 과정

데이터를 수집하는 센터마다 강좌를 분류하는 기준이 상이하며 오분류 된 강좌가 존재 하는 상황이었습니다.

- 문제의 원인:  수집한 데이터를 재분류 해야 하는데 정규 분포식만으로는 해결이 힘들었습니다. 
- 대안:  정규 표현식 대신 머신러닝을 통해 데이터를 재분류를 하기로 결정 했습니다.
- 연구:  미리 학습시킨 모델을 파인 튜닝하면 간단하지만 제가 원하는 기준으로 텍스트 분류가 가능하다는 걸 알게 되었습니다. 
- 해결:  크롤링한 강좌들을 제가 원하는 분류 기준으로 라벨링 한 뒤, kobert 모델을 사용해 학습시켰습니다.
- 평가:  강좌 내용은 계속 달라지기 때문에 지속적인 학습이 필요하겠으나, 정규 표현식으로 진행했을 때보다 정교한 분류가 가능해졌습니다.
   [레포지토리 참조](https://github.com/redoundo/culture_center_server/tree/ml)

2. 라벨링이 필요한 새로운 데이터를 데이터베이스에서 직접 가져오는 게 불편했습니다.

   1. 	문제의 원인: 




### Api 레퍼런스

[postman api 이동](https://documenter.getpostman.com/view/25808797/2sA3JRZebp)



### 사용 기술

`front-end`
- React
- recoil

`back-end`
- Flask
- SQLAlchemy
- Mysql
- Docker
- AWS


## ERD 설계

![culture_center_erm](https://github.com/redoundo/culture_center_server/assets/96558064/f7586cb3-20fd-4594-bea2-ffd6c501dfb9)

### 트러블 슈팅

<details>
    <summary>aws s3 이미지 덮어쓰기 안됨</summary>
    <div markdown="1">
		aws 이미지를 동일한 이름으로 업로드 할 때, 덮어쓰기가 안되고 기존에 있던 이미지가 deploy 되는 문제 발생.
    </div>
</details>



