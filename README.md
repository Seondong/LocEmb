# LocEmb: Location Embedding

* Location Embedding (Currently covering Korean district)

### 프로젝트 목표
* 전국 지역 단위별 embedding을 제공하고자 함
* To-do: 사업자, 지번, 건물 등으로 확장 계획 중

### 사용 가능한 프로젝트
* 전염병 모델 개발시 pretrained된 지역별 embedding값을 covariate으로 활용
* 장소 추천/ 예측 모델에 pretrained된 embedding값을 활용

### 사용한 알고리즘
* Poincare Embedding([NeurIPS2017](https://papers.nips.cc/paper/7213-poincare-embeddings-for-learning-hierarchical-representations))을 기반으로 위도 및 경도를 추가로 활용하여 임베딩을 학습
* 세부 방법론 소개: [슬라이드](http://seondong.github.io/assets/papers/20191213-embedding.pdf)
    - 해당 슬라이드에서 소개한 방법론을 일부 개선하여 적용 중
    - 현재는 해당 슬라이드에서 언급한 데이터와는 상이한 데이터를 활용하고 있음
    
### 파일 설명
* LocEmb-EDA.ipynb: 임베딩 결과값 체크 및 지역별 유사도 계산 예제
* embedding+시군구명.csv: 시군구2vec (251개 시군구, 100 dimensions)
* embedding+법정동명.csv: 법정동2vec (5,005개 법정동, 100 dimensions)
* embedding+행정동명.csv: 법정동2vec (3,582개 행정동, 100 dimensions)
* embedding+도로명+first5000rows.csv: 도로명2vec (110,722개 중 5,000개 도로명, 100 dimensions)
* (Upon on request) embedding+도로명.csv: 도로명2vec (110,722개 도로명, 100 dimensions)

### Contact information
For help or issues using LocEmb, please submit a GitHub issue.
For personal communication related to LocEmb, please contact Sundong Kim(sundong@ibs.re.kr).