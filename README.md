# LocEmb: Location Embedding

* Location Embedding (Currently covering Korean district)

### 프로젝트 목표
* 전국 지역 단위별 embedding을 제공하고자 함
* To-do: 사업자, 지번, 건물 등으로 확장 계획 중

### 임베딩 결과물 소개
* [embedding+시군구명.csv](embedding+시군구명.csv): 시군구2vec (전체 251개 시군구, 100 dimensions)
* [embedding+법정동명.csv](embedding+법정동명.csv): 법정동2vec (전체 5,005개 법정동, 100 dimensions)
* [embedding+행정동명.csv](embedding+행정동명.csv): 행정동2vec (전체 3,582개 행정동, 100 dimensions)
* [embedding+도로명+first5000rows.csv](embedding+도로명+first5000rows.csv): 도로명2vec (전체 110,722개 중 5,000개 도로명, 100 dimensions)
    * (Upon on request) [embedding+도로명.csv](https://github.com/Seondong/LocEmb): 도로명2vec (전체 110,722개 도로명, 100 dimensions)
* [LocEmb-EDA.ipynb](.): 임베딩 결과값 체크 및 지역별 유사도 계산 예제

### 알고리즘
* Poincare Embedding([NeurIPS2017](https://papers.nips.cc/paper/7213-poincare-embeddings-for-learning-hierarchical-representations))을 기반으로 위도 및 경도를 추가로 활용하여 각 구역, 도로별 임베딩을 학습함
* 세부 방법론 소개: [슬라이드](http://seondong.github.io/assets/papers/20191213-embedding.pdf)
    - 해당 슬라이드에서 소개한 방법론을 일부 개선하여 적용 중
    - 슬라이드에서 활용한 데이터는 현 프로젝트에서 활용한 데이터와는 상이한 데이터임

### 활용한 데이터
* 전국 사업체조사 공공데이터: https://www.data.go.kr/dataset/3073433/fileData.do
    
### 활용 가능한 프로젝트
* 장소 추천 / 예측 모델에 pretrained된 embedding값을 활용
* 지역별 전염병 확산 모델 개발시 pretrained된 지역별 embedding값을 covariate으로 활용

### 제반 지식
* Poincare embedding
    - Gensim implementation: https://radimrehurek.com/gensim/models/poincare.html
    - Pytorch implementation: https://github.com/facebookresearch/poincare-embeddings
* PNU코드: https://m.post.naver.com/viewer/postView.nhn?volumeNo=7135987&memberNo=36248235
    - 예시 ![PNU코드](fig/pnu.jpg)
* 건물관리번호 (https://www.vw-lab.com/32):
    - 생성 당시 기준의 PNU + 연번으로 구성됨, 변경되지 않는 고유값
    - 예시 ![건물관리번호](fig/bldgcode.png)
* PNU ↔ 주소간 상호 변환과 메타데이터: https://m.post.naver.com/viewer/postView.nhn?volumeNo=7242031&memberNo=36248235
* 주소 변환: http://juso.go.kr/dn.do?fileName=%EC%A3%BC%EC%86%8C%EC%A0%84%ED%99%98_%EA%B0%80%EC%9D%B4%EB%93%9C.pdf&realFileName=f493270c-d88f-4852-a807-17a6189a8871.pdf&regYmd=2012

### Contact information
For help or issues using LocEmb, please submit a GitHub issue.
For personal communication related to LocEmb, please contact Sundong Kim(sundong@ibs.re.kr).