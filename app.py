import streamlit as st
import pandas as pd
import io
import os
from PIL import Image
import streamlit.components.v1 as components
import altair as alt
import plotly.graph_objects as go
import plotly.express as px

st.write('# 지하철 이용인원 예측')
st.write(' ')
st.write(' ')

with st.sidebar:
    add_select = st.radio(
    'Menu',
    ('지하철 데이터 전처리','지하철 이용인원','출퇴근 시간 승하차',
     '붐비는 시간','기상 데이터 전처리')
)

if add_select == '지하철 데이터 전처리':
    st.write('### 지하철 시간별 승하차 인원 (원본)')
    filepath = 'data/서울교통공사_역별 일별 시간대별 승하차인원 정보_UTF8.csv'
    df = pd.read_csv(filepath, encoding='utf-8', index_col=0)

    st.dataframe(df)

    buf = io.StringIO()
    df.info(buf=buf)
    s = buf.getvalue()

    st.text(s)

    img = Image.open(os.path.join(os.path.dirname(__file__), '특일정보.JPG'))

    st.write(' ')
    st.write(' ')

    st.image(img, use_column_width=True)

    st.write(' ')
    st.write(' ')

    st.write('#### 23년도 공휴일')
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

    code_minus = """
    df_up = ndf[ndf['승하차구분'] == '승차']
    df_down = ndf[ndf['승하차구분'] == '하차']

    df_diff = df_up.set_index(['수송일자', '호선', '고유역번호(외부역코드)', '역명']).loc[:,'06시이전':'총 이용인원']
    - df_down.set_index(['수송일자', '호선', '고유역번호(외부역코드)', '역명']).loc[:,'06시이전':'총 이용인원']

    df_diff['승하차구분'] = '승하차 차이'

    result = pd.concat([ndf, df_diff])
    result = result.sort_values(by=['수송일자', '호선', '고유역번호(외부역코드)', '역명'])
    """
    st.code(code_minus, language='python')

if add_select == '지하철 이용인원':
    st.write('## 서울시 전체 노선')
    seoul1, seoul2 = st.tabs(['역별 이용인원', '지하철 이용인원 및 인구'])

    with seoul1:
        st.write('#### 역별 이용인원')
        with open('map_visual/seoul_result_tot.html', 'r', encoding='utf-8') as f:
            tot = f.read()
        components.html(tot, width=1000, height=700)

    with seoul2:
        st.write('#### 역별 이용인원 및 주민등록인구')
        with open('map_visual/seoul_subway_pop.html', 'r', encoding='utf-8') as f:
            tot_pop = f.read()
        components.html(tot_pop, width=1000, height=700)

if add_select == '출퇴근 시간 승하차':
    st.write('## 출근시간 승하차 차이')
    morning07, morning08 = st.tabs(['07시', '08시'])

    with morning07:
        st.write('#### 월요일 07시')
        with open('map_visual/seoul_diff_07_pop.html', 'r', encoding='utf-8') as f:
            diff_07 = f.read()
        components.html(diff_07, width=1000, height=700)

    with morning08:
        st.write('#### 월요일 08시')
        with open('map_visual/seoul_diff_08_pop.html', 'r', encoding='utf-8') as f:
            diff_08 = f.read()
        components.html(diff_08, width=1000, height=700)

    st.write(' ')
    st.write('## 퇴근시간 승하차 차이')
    night18, night19 = st.tabs(['18시', '19시'])

    with night18:
        st.write('#### 월요일 18시')
        with open('map_visual/seoul_diff_18_pop.html', 'r', encoding='utf-8') as f:
            diff_18 = f.read()
        components.html(diff_18, width=1000, height=700)

    with night19:
        st.write('#### 월요일 19시')
        with open('map_visual/seoul_diff_19_pop.html', 'r', encoding='utf-8') as f:
            diff_19 = f.read()
        components.html(diff_19, width=1000, height=700)


    filepath = 'data/전처리/아침승하차차이 상위_하위.csv'
    morning = pd.read_csv(filepath, encoding='utf-8', index_col=0)

    morning = morning.sort_values('08-09시간대', ascending=False)

    chart = alt.Chart(morning).mark_bar().encode(
        x=alt.X('역명', sort='-y'),
        y=alt.Y('08-09시간대', title='승하차 차이'),
        color=alt.condition(
            alt.datum['08-09시간대'] > 0,  # 조건
            alt.value('blue'),  # 참일 때 값
            alt.value('red')  # 거짓일 때 값
        )
    ).properties(width=800, height=600)

    st.write(' ')
    st.markdown("<h1 style='text-align: center; color: black;'>출근시간 승하차 차이</h1>", unsafe_allow_html=True)
    st.altair_chart(chart, use_container_width=True)

    file_guro = 'data/전처리/구로_승하차차이0723.csv'
    guro = pd.read_csv(file_guro, encoding='utf-8', index_col=0)

    chart_guro = (
        alt.Chart(guro.reset_index())
        .mark_line(color='green', strokeDash=[5,1])
        .encode(
            x=alt.X('index:O', title='시간대'),  
            y=alt.Y('14:Q', title='승하차 차이'),  
        ) 
    )
    st.write(' ')
    st.markdown("<h1 style='text-align: center; color: black;'>구디역 시간별 승하차 추이</h1>", unsafe_allow_html=True)
    st.altair_chart(chart_guro, use_container_width=True)

if add_select == '붐비는 시간':
    code_hap = """
    data_up = data[data['승하차구분'] == '승차']
    data_down = data[data['승하차구분'] == '하차']

    data_hap = data_up.set_index(['수송일자', '호선', '고유역번호(외부역코드)', '역명']).loc[:, '06시이전':'총 이용인원'] 
               + data_down.set_index(['수송일자', '호선', '고유역번호(외부역코드)', '역명']).loc[:, '06시이전':'총 이용인원']
    
    normal = result[(result['승하차구분'] == '합계')&(result['휴무일'] == 0.0)]
    weekend = result[(result['승하차구분'] == '합계')&(result['휴무일'] == 1.0)]
    
    normal_st = normal.groupby(['호선', '역명'], as_index=False)[['06시이전', '06-07시간대',
       '07-08시간대', '08-09시간대', '09-10시간대', '10-11시간대', '11-12시간대', '12-13시간대',
       '13-14시간대', '14-15시간대', '15-16시간대', '16-17시간대', '17-18시간대', '18-19시간대',
       '19-20시간대', '20-21시간대', '21-22시간대', '22-23시간대', '23-24시간대', '24시이후']].mean()
       
    normal_st['붐비는 시간대'] = normal_st.select_dtypes(include=['int','float']).idxmax(axis=1)
    weekend_st['붐비는 시간대'] = weekend_st.select_dtypes(include=['int','float']).idxmax(axis=1)
    """
    st.code(code_hap, language='python')
    
    col1, col2 = st.columns(2)
    with col1:
        st.write('##### 평일 가장 붐비는 시간')
        normal_path = 'data/전처리/전처리_평일_붐비는시간_0729.csv'
        normal_st = pd.read_csv(normal_path, index_col=0)
        st.dataframe(normal_st[['역명','호선','붐비는 시간대']])        

    with col2:
        st.write('##### 주말 가장 붐비는 시간')
        hol_path = 'data/전처리/전처리_주말_붐비는시간_0729.csv'
        weekend_st = pd.read_csv(hol_path, index_col=0)
        st.dataframe(weekend_st[['역명','호선','붐비는 시간대']])     
    
    st.write(' ')
    st.write(' ')
    st.write('## 역별 가장 붐비는 시간')
    normal, holiday = st.tabs(['평일', '휴무일'])
    
    line_colors = {
    '1호선': '#0052A4',
    '2호선': '#00A84D',
    '3호선': '#EF7C1C',
    '4호선': '#00A4E3',
    '5호선': '#996CAC',
    '6호선': '#CD7C2F',
    '7호선': '#747F00',
    '8호선': '#E6186C'}

    with normal:
        st.write('#### 평일')
        fig1 = px.bar(normal_st, x='붐비는 시간대', color='호선', color_discrete_map=line_colors,
                category_orders={'호선': normal_st['호선'].unique()},
                labels={'붐비는 시간대': '붐비는 시간대', '이용인원': '역 개수', '호선': '호선'},
                title='평일 가장 붐비는 시간',
                template='plotly_white', hover_name='역명')
        fig1.update_layout(
            title_x=0.5,
            xaxis_title='가장 붐비는 시간',
            yaxis_title='역 개수',
            )
        st.plotly_chart(fig1)    

    with holiday:
        st.write('#### 휴무일')
        fig2 = px.bar(weekend_st, x='붐비는 시간대', color='호선', color_discrete_map=line_colors,
             category_orders={'호선': normal_st['호선'].unique()},
             labels={'붐비는 시간대': '시                간', 'count': '역 개수', '호선': '호선'},
             title='휴무일 가장 붐비는 시간대',
             template='plotly_white', hover_name='역명')
        fig2.update_layout(
            title_x=0.5,
            xaxis_title='가장 붐비는 시간',
            yaxis_title='역 개수',
            )
        st.plotly_chart(fig2)
    
    st.write(' ')
    st.write(' ')
    st.write('## 역별 유무임 승하차 인원')
    money1, money2 = st.tabs(['원본','전처리'])
    with money1:
        money1_path = 'data/지하철/지하철_유무임별_이용현황.xls'
        money1 = pd.read_excel(money1_path)
        st.dataframe(money1)
    with money2:
        money2_path = 'data/지하철/전처리_역별_무임승하차율.csv'
        money2 = pd.read_csv(money2_path, index_col=0)
        st.dataframe(money2)

if add_select == '기상 데이터 전처리':
    st.write('### 서울 기상 관측 정보 (원본)')
    weather1_path = 'data/기상/원본_기상/관악_2306_origin.csv'
    weather1 = pd.read_csv(weather1_path, encoding='ansi')
    st.dataframe(weather1)
    st.write(' ')
    st.write('##### 시간당 강수량')
    code_weather = """
    ndf = ndf.groupby(ndf['일시'].dt.floor('H')).
          agg({'기온(°C)':'mean', '누적강수량(mm)':'max', '습도(%)':'mean'})
          
    ndf['강수량차이'] = ndf['누적강수량(mm)'].shift(+1)
    
    ndf['시간당 강수량(mm)'] = ndf['누적강수량(mm)'] - ndf['강수량차이']
    """
    st.code(code_weather, language='python')
    
    st.write(' ')
    st.write('##### 강수량 분류')
    code_rain = """
    def rain(x):
        if x == 0:
            return '해당 없음'
        elif x < 3:
            return '약한 비'
        elif x < 15:
            return '보통 비'
        elif x < 30:
            return '강한 비'
        elif x >=30:
            return '매우 강한 비'    
            
    final_data['강수량 분류'] = final_data['시간당 강수량(mm)'].apply(rain)
    """
    st.code(code_rain, language='python')
    
    st.write(' ')
    st.write('##### 폭염일')
    code_heat = """
    def heat_wave(x):
    heat_dates = [
        '2022-07-02',
        '2022-07-03',
        '2022-07-05',
        '2022-07-06',
        '2022-07-10',
        '2022-07-26',
        '2022-07-27',
        '2022-07-28',
        '2022-07-29',
        '2022-07-30',
    ]
    if x.strftime('%Y-%m-%d') in heat_dates:
        return 'True'
    else:
        return 'False'
    """
    st.code(code_heat, language='python')

    st.write(' ')
    st.write('##### 한파일')
    code_cold = """
    def cold_wave(x):
        cold_dates = [
            '2022-12-18',
            '2022-12-19',
            '2022-12-23',
            '2022-12-24',
            '2023-01-24',
            '2023-01-25',
        ]
        if x.strftime('%Y-%m-%d') in cold_dates:
            return 'True'
        else:
            return 'False'
    """
    st.code(code_cold, language='python')
    
    st.write(' ')
    st.write('### 서울 기상 관측 정보 (전처리)')
    weather2_path = 'data/기상/서울날씨_2205_2304_rev.csv'
    weather2 = pd.read_csv(weather2_path)
    st.dataframe(weather2)