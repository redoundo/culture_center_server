## culture_center project

### 기능
      기업 문화 센터 뿐만 아니라 도서관 등에서 실행 되는 문화 강좌를 모아 제공.
_____

### 과정
    

### 개선 /문제 해결 사례
   1. 상이한 분류 기준을 가진 내용의 재분류 개선 사례
      1) 문제 : 크롤링 해온 내용의 재분류가 정규 표현식 만으로는 해결 불가능한 상황. 
      2) 원인 : 크롤링을 진행한 각각의 문화 센터마다 상이한 분류 기준을 가지고 있었을 뿐만 아니라 해당 문화 센터의 분류 기준을 지키지 않는 강좌들이 다수 존재. 때문에 해당 강좌가 게시된 문화 센터의 분류조차도 재분류 하는데 도움이 되지 않았다.
      3) 대안 : 정규 표현식 대신 머신러닝을 통해 재분류를 진행하기로 결정.
      4) 연구 : 머신러닝에 대해 학습하며 내용 분류는 지도학습에 해당한다는???
      5) 해결 : 크롤링한 내용을 원하는 분류 기준으로 라벨링 시킨 뒤 파인튜닝된 kobert 모델에게 학습시켰다.
      6) 평가 : 정확성을 유지하기 위해서는 계절이나 상황에 따라 달라지는 내용을 지속적으로 재분류하여 학습시켜 줘야 했으나 정규 표현식으로 진행했을 때보다는 정교한 분류가 가능해졌다.
   2. 