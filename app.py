import streamlit as st
import pandas as pd
import io

st.write('# 지하철 이용인원 예측')
st.write(' ')
st.write(' ')
st.write('### 지하철 원본 데이터')


filepath = 'data/서울교통공사_역별 일별 시간대별 승하차인원 정보_UTF8.csv'
df = pd.read_csv(filepath, encoding='utf-8', index_col=0)

st.dataframe(df)

buf = io.StringIO()
df.info(buf=buf)
s = buf.getvalue()

st.text(s)

from PIL import Image

img = Image.open('특일정보.JPG')
st.image(img, use_column_width=True)

hol_23 = pd.read_csv('data/holidays_2023.csv', index_col=0)
st.dataframe(hol_23)

code1 = """
def hol(x):
    if x in holidays.values or x.weekday() in [5,6]:
        return 1    
    else:
        return 0

data['휴무일'] = data['수송일자'].apply(hol)
"""
st.code(code1, language='python')

df2 = pd.read_csv('data/전처리/전처리_지하철_요일_고유역번호_승하차차이_휴무일0721.csv', index_col=0)

st.write('### 전처리 후')
st.dataframe(df2)

code2 = """
df_up = ndf[ndf['승하차구분'] == '승차']
df_down = ndf[ndf['승하차구분'] == '하차']

df_diff = df_up.set_index(['수송일자', '호선', '고유역번호(외부역코드)', '역명']).loc[:,'06시이전':'총 이용인원']
- df_down.set_index(['수송일자', '호선', '고유역번호(외부역코드)', '역명']).loc[:,'06시이전':'총 이용인원']

df_diff['승하차구분'] = '승하차 차이'

result = pd.concat([ndf, df_diff])
result = result.sort_values(by=['수송일자', '호선', '고유역번호(외부역코드)', '역명'])
"""
st.code(code2, language='python')

import streamlit.components.v1 as components

with open('map_visual/seoul_result_tot.html', 'r', encoding='utf-8') as f:
    tot = f.read()
st.write('### 서울시 지하철 노선')
components.html(tot, width=1000, height=700)

with open('map_visual/seoul_subway_pop.html', 'r', encoding='utf-8') as f:
    tot_pop = f.read()
st.write('### 서울시 지하철 노선과 주민등록인구')
components.html(tot_pop, width=1000, height=700)

with open('map_visual/seoul_diff_07_pop.html', 'r', encoding='utf-8') as f:
    diff_07 = f.read()
st.write('### 월요일 07시 승하차 차이')
components.html(diff_07, width=1000, height=700)

with open('map_visual/seoul_diff_08_pop.html', 'r', encoding='utf-8') as f:
    diff_08 = f.read()
st.write('### 월요일 08시 승하차 차이')
components.html(diff_08, width=1000, height=700)

with open('map_visual/seoul_diff_18_pop.html', 'r', encoding='utf-8') as f:
    diff_18 = f.read()
st.write('### 월요일 18시 승하차 차이')
components.html(diff_18, width=1000, height=700)

with open('map_visual/seoul_diff_19_pop.html', 'r', encoding='utf-8') as f:
    diff_19 = f.read()
st.write('### 월요일 19시 승하차 차이')
components.html(diff_19, width=1000, height=700)
