import pandas as pd
filepath = 'data/서울교통공사_역별 일별 시간대별 승하차인원 정보.csv'
df = pd.read_csv(filepath, encoding='ansi', index_col=0)
df.to_csv('data/서울교통공사_역별 일별 시간대별 승하차인원 정보_UTF8.csv', encoding='utf-8')