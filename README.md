# culture-center-project

### 프로젝트 소개

  	기업 소재의 문화 센터 뿐만 아니라 도서관 등에서 실행 되는 문화 강좌를 모아 제공합니다.
  	파편화 된 문화 강좌들을 쉽게 찾고 싶어서 진행한 프로젝트 입니다.
  	강좌 내용이 지속적으로 업데이트 되고 그에 맞는 크롤링이 필요하기 때문에 

---

### 핵심 기능

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

라벨링이 필요한 새로운 데이터를 데이터베이스에서 직접 가져오는 게 불편했습니다.

1. 	문제의 원인: 

### 웹사이트 기능

<details>
    <summary>검색</summary>
		<img src="https://github.com/redoundo/culture_center_server/assets/96558064/3adb735a-a8c9-4201-94ff-479100c47088"/>
</details>


<details>
    <summary>강의 등록 및 삭제</summary>
    <img src="https://github.com/redoundo/culture_center_server/assets/96558064/cb0a7134-7098-4e33-9480-96f6ea350dfd"/>
</details>


<details>
    <summary>회원정보 변경 및 탈퇴</summary>
    <img src="https://github.com/redoundo/culture_center_server/assets/96558064/9d5c2a63-9c8c-4b78-a375-87049c8a4a98"/>
</details>



### 어려웠던 점

<details>
    <summary>비슷한 구조의 크롤링 과정</summary>
    쿼리 스트링을 사용할 수 있는 사이트와 아닌 사이트를 구분하여 각각 다른 
</details>

   느린 검색 결과 









### Api 레퍼런스

[postman api 이동](https://documenter.getpostman.com/view/25808797/2sA3JRZebp)



### 사용 기술

`front-end`

- React

- Recoil

  

`back-end`

- Flask 

- SQLAlchemy

- Mysql

- Docker

  

`deploy`

- Aws EC2

- Aws RDS

- Aws CodeDeploy

- Github Actions

  

`crawler`

- Playwright



## ERD 설계

![](C:\Users\admin\Downloads\culture_center_erm.png)

### 트러블 슈팅

<details>
    <summary>aws code deploy 최신 버전이 가져와 지지 않음.</summary>
    <div markdown="1">
		codedeploy 그룹 재생성으로 해결
    </div>
</details>


<details style="background-color:white">
    <summary>windows os 인 ec2 인스턴스에서 ubuntu 이미지 사용시 에러 발생</summary>
    <div style="padding: 15px;font-style: italic">
        latest: Pulling from library/ubuntu 2024-05-23 03:16:56 [stderr]no matching manifest for windows/amd64 10.0.20348 in the manifest list entries
    </div>
    <div style="padding: 9px">
        windows os 에 설치된 docker 에서는 linux 계열 이미지를 사용하지 못하기 때문에 발생하는 에러 입니다.
wsl을 통해 linux 계열 이미지를 사용할 수는 있으나 wsl 과 ubuntu를 설치해본 결과 인스턴스의 심각한 용량 부족으로 인해 새로운 ec2 인스턴스를 생성하기로 결정했습니다.
    </div>
</details>




### 추후 계획

   아직 공공기관의 강의까지 크롤링을 진행하지 않았지만  크롤링 확대.

