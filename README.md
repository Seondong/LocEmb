# LocEmb: Location Embedding

* Location Embedding (Currently covering Korean district)
* 만든 이: 김선동 (http://seondong.github.io)

### 프로젝트 목표
* 전국 지역 단위별 embedding을 제공하고자 함
* 도로명, 상권, 사업자 등으로 확장 가능

### 사용 가능한 프로젝트
* 전염병 모델 개발시 pretrained된 지역별 embedding값을 covariate으로 활용
* 장소 추천/ 예측 모델에 pretrained된 embedding값을 활용

### 사용한 알고리즘
* [NeurIPS2017](https://papers.nips.cc/paper/7213-poincare-embeddings-for-learning-hierarchical-representations)을 기반으로 다양한 feature를 추가하였음

### 파일 설명
* LocEmb-EDA.html: 임베딩 결과값 체크 및 지역별 유사도 계산 예제
* embedding+법정동명전체.csv: Fine-grained embedding (5005개 법정동 Cover, 100 dimensions)
* embedding+시군구명전체.csv: Coarse-grained embedding (251개 시군구 Cover, 100 dimensions)