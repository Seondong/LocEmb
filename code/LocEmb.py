import pandas as pd
import numpy as np
import logging
import pickle
import sys
import os
from gensim.models.poincare import PoincareModel
from gensim.test.utils import datapath

def embedding(relations,size,epochs):
    model = PoincareModel(relations,size=size,negative=5)
    model.train(epochs=epochs,batch_size=64,print_every=1)
    return model

# 데이터 로드
df1 = pd.read_csv('./상가업소정보_201912_01.csv', sep='|')
df2 = pd.read_csv('./상가업소정보_201912_02.csv', sep='|')
df3 = pd.read_csv('./상가업소정보_201912_03.csv', sep='|')
df4 = pd.read_csv('./상가업소정보_201912_04.csv', sep='|')
df = pd.concat([df1, df2, df3, df4])



###
# 1. 법정동, 시군구, 시도 관계 추가
for col in ['지번코드', '법정동코드', '시군구코드', '시도코드']:
    df[col] = df[col].astype('Int64')

d_bdongs = dict(zip(df['법정동코드'], df['시도명'] + ' '+ df['시군구명'] + ' ' + df['법정동명']))
d_sis = dict(zip(df['시군구코드'], df['시도명'] + ' '+ df['시군구명']))
d_dos = dict(zip(df['시도코드'], df['시도명']))

d_bdong_si = dict(zip(df['법정동코드'].apply(lambda x: d_bdongs[x]), df['시군구코드'].apply(lambda x: d_sis[x])))
d_si_do = dict(zip(df['시군구코드'].apply(lambda x: d_sis[x]), df['시도코드'].apply(lambda x: d_dos[x])))
d_do_root = {do:0 for do in set(d_si_do.values())}

hierarchical_list = []
for d in [d_do_root, d_si_do, d_bdong_si]: 
    hierarchical_list.extend(d.items())
print('기본 구역 정보 - 법정동, 시군구, 시도 추가 후 relation 개수: ', len(hierarchical_list))  


size = 100
epochs = 30

# # 임베딩 학습 및 저장
# EMB_SOURCE = 'district'
# m1 = embedding(hierarchical_list,size=int(size),epochs=int(epochs))
# pickle.dump(m1, open('poincare_embedding_result_'+str(size)+'+'+str(epochs)+EMB_SOURCE+'.p', 'wb'))



###
# 2. 위, 경도 추가
df.loc[:, '경도_2'] = df['경도'].apply(lambda x: round(x, 2))
df.loc[:, '경도_1'] = df['경도'].apply(lambda x: round(x, 1))
df.loc[:, '경도_0'] = df['경도'].apply(lambda x: round(x, 0))
df.loc[:, '위도_2'] = df['위도'].apply(lambda x: round(x, 2))
df.loc[:, '위도_1'] = df['위도'].apply(lambda x: round(x, 1))
df.loc[:, '위도_0'] = df['위도'].apply(lambda x: round(x, 0))

latlng = set()
largest_latlng = set()

for i in range(0, 2):
    lat1 = df['경도_'+str(i+1)]
    lng1 = df['위도_'+str(i+1)]
    lat2 = df['경도_'+str(i)]
    lng2 = df['위도_'+str(i)]

    for at1, ng1, at2, ng2 in zip(lat1, lng1, lat2, lng2):
        tup1 = tuple((ng1, at1))
        tup2 = tuple((ng2, at2))
        latlng.add((tup1, tup2))

        if i == 0:
            largest_latlng.add(tup2)
            
# 법정동, 시군구와 위, 경도의 관계 추가
df['법정동명전체'] = (df['시도명'] + ' '+ df['시군구명'] + ' ' + df['법정동명'])
df['시군구명전체'] = (df['시도명'] + ' '+ df['시군구명'])

latlng_list = list(latlng) +   (list(set(((y,z), x) for x, y, z in df[['법정동명전체','위도_1', '경도_1']].dropna(axis=0).values)) 
                              + list(set(((y,z), x) for x, y, z in df[['법정동명전체','위도_2', '경도_2']].dropna(axis=0).values))
                              + list(set(((y,z), x) for x, y, z in df[['시군구명전체','위도_1', '경도_1']].dropna(axis=0).values))
                              + list(set(((y,z), x) for x, y, z in df[['시군구명전체','위도_2', '경도_2']].dropna(axis=0).values))
                              + list(set(((y,z), x) for x, y, z in df[['시도명','위도_1', '경도_1']].dropna(axis=0).values)))

for item in largest_latlng:
    latlng_list.append((item, 0))

hierarchical_list += latlng_list
print('법정동+위경도 추가 후 relation 개수: ', len(hierarchical_list))  

# # 임베딩 학습 및 저장
# EMB_SOURCE = 'district+latlng'
# m2 = embedding(hierarchical_list,size=int(size),epochs=int(epochs))
# pickle.dump(m2, open('poincare_embedding_result_'+str(size)+'+'+str(epochs)+EMB_SOURCE+'.p', 'wb'))



###
# 3. 행정동 및 위, 경도와의 관계 추가
df['행정동명전체'] = (df['시도명'] + ' '+ df['시군구명'] + ' ' + df['행정동명'] + ' (행정동)')

dong_pairs = list((x,y) for x, y in df[['행정동명전체', '법정동명전체']].dropna(axis=0).drop_duplicates().values)
hierarchical_list += dong_pairs

latlng_list2 = (list(set(((y,z), x) for x, y, z in df[['행정동명전체','위도_1', '경도_1']].dropna(axis=0).values)) 
              + list(set(((y,z), x) for x, y, z in df[['행정동명전체','위도_2', '경도_2']].dropna(axis=0).values))
               )

hierarchical_list += latlng_list2
print('행정동+위경도 추가 후 relation 개수: ', len(hierarchical_list))      

# # 임베딩 학습 및 저장
# EMB_SOURCE = 'district(행정+법정)+latlng'
# m3 = embedding(hierarchical_list,size=int(size),epochs=int(epochs))
# pickle.dump(m3, open('poincare_embedding_result_'+str(size)+'+'+str(epochs)+EMB_SOURCE+'.p', 'wb'))



###
# 4. 도로명 추가

district_road_pairs = list((x,y) for x, y in df[['도로명', '법정동명전체']].dropna(axis=0).drop_duplicates().values)
latlng_list3 = list(set(((y,z),x) for x, y, z in df[['도로명', '위도_2', '경도_2']].dropna(axis=0).values))
hierarchical_list += district_road_pairs
hierarchical_list += latlng_list3
print('도로명 추가 후 relation 개수: ', len(hierarchical_list))      

# # 임베딩 학습 및 저장
# EMB_SOURCE = 'district(행정+법정)+도로명+latlng'
# m4 = embedding(hierarchical_list,size=int(size),epochs=int(epochs))
# pickle.dump(m4, open('poincare_embedding_result_'+str(size)+'_'+str(epochs)+'+'+EMB_SOURCE+'.p', 'wb'))



###
# 5. 업종 및 상호 추가, 도로명과 연동
# 지점명이 있으면(34만 건): (지번주소, 도로명주소) -> 상호지점명 -> 상호명
# 지점명이 없으면(240만 건): (지번주소, 도로명주소) -> 상호명 

df['상호지점명'] = df['상호명'] + ' ' + df['지점명']

f1 = list(((y,x),(z,y),(w,y)) for x,y,z,w in df[~df['지점명'].isna()][['상호명', '상호지점명', '도로명주소', '지번주소']].dropna(axis=0).drop_duplicates().values)
f1 = [item for sublist in f1 for item in sublist]

f2 = list(((y,x),(z,x)) for x,y,z in df[df['지점명'].isna()][['상호명', '도로명주소', '지번주소']].dropna(axis=0).drop_duplicates().values)
f2 = [item for sublist in f2 for item in sublist]

f3 = list((y,x) for x, y in df[['도로명', '도로명주소']].dropna(axis=0).drop_duplicates().values)
f4 = list((y,x) for x, y in df[['법정동명', '지번주소']].dropna(axis=0).drop_duplicates().values)

f5 = list(((y,x),(z,y),(w,z)) for x, y, z, w in df[['상권업종대분류명', '상권업종중분류명', '상권업종소분류명', '상호명']].dropna(axis=0).drop_duplicates().values)
f5 = [item for sublist in f5 for item in sublist]

# (도로명주소, 지번주소) -> (위도, 경도), 해당 위경도에는 여러 도로명주소나 지번주소가 있을 수 있음
f6  = list(((z, (x,y)), (w, (x,y))) for x, y, z, w in df[['위도_2', '경도_2', '도로명주소', '지번주소']].dropna(axis=0).drop_duplicates().values)
f6 = [item for sublist in f6 for item in sublist]

f7 = list((item, 0) for item in set(df['상권업종대분류명']))

print(len(f1), len(f2), len(f3), len(f4), len(f5), len(f6), len(f7))

hierarchical_list += f1
hierarchical_list += f2
hierarchical_list += f3
hierarchical_list += f4
hierarchical_list += f5
hierarchical_list += f6
hierarchical_list += f7

print('업종, 상호, 지번, 도로명 주소 추가 후 relation 개수: ', len(hierarchical_list)) 

# 임베딩 학습 및 저장
EMB_SOURCE = 'district(행정+법정)+도로명+지번도로명주소+업종+상호명+latlng'
m5 = embedding(hierarchical_list,size=int(size),epochs=int(epochs))
pickle.dump(m5, open('poincare_embedding_result_'+str(size)+'_'+str(epochs)+'+'+EMB_SOURCE+'.p', 'wb'))

EMB_SOURCE = 'district(행정+법정)+도로명+latlng'
m4 = embedding(hierarchical_list,size=int(size),epochs=int(epochs))
pickle.dump(m4, open('poincare_embedding_result_'+str(size)+'_'+str(epochs)+'+'+EMB_SOURCE+'.p', 'wb'))
