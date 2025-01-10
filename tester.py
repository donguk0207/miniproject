from db_connector import fetch_data_from_mysql

# 서울시 따릉이 데이터 가져오기
data_seoul = fetch_data_from_mysql()

# 데이터 확인
print(data_seoul.head())  # 데이터가 제대로 불러와졌는지 확인




him['region'] = np.where(him['Gu'] == '마포구', 1, 0)
print(him['region'].value_counts())

him['age'] = np.where(him['Age_Group'] == '20대', 1, 0)
print(him['age'].value_counts())

him['moving'] = np.where(moving['start'] == '마포구', 1, 0)
print(him['moving'].value_counts())
#종속변수와 독립변수 구분 및 constant 추가

cols = ['Hour','Station_no_out','age']

X = him[cols]
Y = him['region']
X = sm.add_constant(X) #constant(intercept)

#로지스틱회귀분석 모델 학습
model = sm.Logit(Y,X)
model = model.fit()

print(model.summary())