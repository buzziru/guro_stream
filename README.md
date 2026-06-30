# 서울 지하철 이용인원 예측 (Seoul Subway Ridership Forecasting)

> *시간대별·역별로 바뀌는 지하철 이용 퍼즐 풀기*

탑승 전에 역별·시간대별 지하철 이용인원(혼잡도)을 미리 알 수 있다면? 이 물음에서 출발해, **여러 출처에 흩어진 공공데이터를 직접 수집하고 대규모로 전처리·통합**해 하나의 분석 데이터셋을 만들고, 이를 바탕으로 이용인원을 예측한 프로젝트입니다.

> 데이터 분석 입문기에 진행한 **첫 팀 프로젝트**입니다. 모델 자체의 완성도보다, **다양한 출처의 데이터를 직접 모아 대규모로 전처리·통합**하는 데이터 다루기 경험에 무게를 두었습니다.

### 🔗 대시보드

[![메인 대시보드](https://img.shields.io/badge/메인_대시보드-인사이트_큐레이션-5e6ad2?style=for-the-badge)](https://ingyoun-seoul-subway-demo.static.hf.space)

- **메인 대시보드** — [ingyoun-seoul-subway-demo.static.hf.space](https://ingyoun-seoul-subway-demo.static.hf.space) · 핵심 인사이트를 큐레이션한 단일 화면 대시보드 (Hugging Face Static Space, `static-demo/`)
- 초기 EDA 대시보드 — [gurostream-process.streamlit.app](https://gurostream-process.streamlit.app/) · 수집·전처리 과정을 담은 Streamlit 앱 (`app.py`)

---

## 📌 프로젝트 개요

| 항목 | 내용 |
| --- | --- |
| **목표** | 역별·시간대별 지하철 이용인원(혼잡도) 사전 예측 → 쾌적한 대중교통 이용에 기여 |
| **기간 / 대상** | 발표 2023.09 · 서울 지하철 1–8호선 · '22.05 ~ '23.04 |
| **팀** | Team 김조하 (김승연 · **조인경[조장]** · 하영주) |
| **본인 역할** | 조장 · 주제 선정 · 데이터 수집 · 전처리 · **머신러닝 총괄** · 자료 저장소(Notion) 운영 |
| **결과물** | 356만 행 통합 데이터셋 · 예측 모델(LGBM) · 지도/차트 시각화 · 대시보드 |

---

## 📦 데이터 수집 & 통합 (프로젝트의 핵심)

예측 모델보다 **데이터를 모으고 합치는 일**이 이 프로젝트의 핵심이었습니다.

- **수집 출처** : 공공데이터포털 · 서울 열린데이터광장 등 **다수** (인터넷 검색 · 정보공개청구 포함)
- **수집 규모** : 약 **350만 건** · **수집 기간 약 8주**
- **수집 영역** : 서로 다른 4개 도메인

| 영역 | 주요 항목 |
| --- | --- |
| **지하철 이용** | 역별·일별·시간대별 승하차 인원, 요일·휴무일·유무임 구분 (1–8호선, 05~24시) |
| **기후** | 기온 · 습도 · 강수량(기준별 분류) · 폭염/한파 여부 |
| **부동산 · 경제활동** | 구별 부동산 평균가 · 인구수 · 용지 구분 · 업종/사업체 |
| **기타** | 역별 버스정류장 수 · 버스 노선 수 · 버스 승하차 · 출입구 수 · 역세권 수 |

**→ 전처리 결과** : 역·시간대를 복합 키로 4개 영역을 조인하고 결측 처리·파생 피처(요일·공휴일·폭염/한파)를 생성해, **3,564,584행 × 50개 컬럼**의 단일 분석 데이터셋으로 통합했습니다.

---

## 🤖 모델링

`전월_이용인원`, `시간`, `요일`, `호선`, `역명`, `승하차구분`, `시간당 강수량`, `버스정류장수`, `역세권_수` 등을 독립변수로, `지하철이용인원`을 예측했습니다. (로그 변환 · StandardScaler · Label/OneHot Encoding)

| 모델 | Test R² | 5-Fold CV | 검증셋('22.01~04) |
| --- | --- | --- | --- |
| 선형회귀 | 0.903 | 0.796 | 0.863 |
| **LightGBM** ✅ | **0.956** | **0.957** | **0.925** |

- 선형회귀는 단순 평가(0.903) 대비 교차검증(0.796)에서 점수가 크게 떨어져 **복잡한 비선형·시간 패턴 포착에 한계**.
- **LightGBM**은 교차검증·별도 검증셋에서도 안정적이라 **최종 모델로 채택**. (Durbin–Watson 자기상관 검정 병행)
- 가장 중요한 변수는 `전월_이용인원` · `시간` · `요일`.

---

## 🔎 주요 인사이트

- **구로디지털단지역**: 아침(08–09시) 하차가 몰리고 저녁(18–19시) 승차가 몰리는 **전형적 업무지구 통근 패턴**.
- **출근(08–09시) 순하차 상위**(업무지구로 모여듦): 가산디지털단지 · 역삼 · 삼성 · 을지로입구 · 선릉.
- **출근 순승차 상위**(주거지에서 빠져나감): 신림 · 까치산 · 화곡 · 서울대입구 · 연신내.
- **날씨**는 이용 목적에 따라 영향이 다름 — 출퇴근엔 영향이 적으나 **주간 이용은 강수량 영향이 큼**.
- **요일**: 평일 간 차이는 작지만 **평일–주말 차이는 뚜렷**.

---

## 🖥 대시보드

### 메인 — 정적 인사이트 대시보드 (`static-demo/`)
사이드바로 뷰를 전환하는 단일 화면 대시보드. folium 지도(이용인원·출퇴근 차이)와 실측 집계 차트(구디역 시간대별, 출근 순승하차 상위)를 큐레이션했습니다. Hugging Face Static Space로 배포되며 포트폴리오에 임베드됩니다. ([static-demo/README.md](static-demo/README.md))

### 초기 — Streamlit EDA 앱 (`app.py`)
수집·전처리 전 과정을 담은 EDA 대시보드 (지하철/기상 전처리, 이용인원·출퇴근 지도, 붐비는 시간 등 5개 메뉴).

---

## 📁 저장소 구조

```
guro_stream/
├── app.py                # Streamlit EDA 대시보드
├── static-demo/          # 메인 정적 대시보드 (HF Static Space)
├── data/                 # 원본·전처리 데이터 (지하철 / 기상 / 전처리 …)
├── map_visual/           # folium 지도 산출물 (HTML)
├── 그래프/                # 분석 그래프 (PNG)
├── malgun.ttf            # 한글 폰트 (matplotlib)
└── requirements.txt
```

---

## 🛠 기술 스택

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![LightGBM](https://img.shields.io/badge/LightGBM-9ACD32?style=for-the-badge&logoColor=white)
![statsmodels](https://img.shields.io/badge/statsmodels-3F51B5?style=for-the-badge&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logoColor=white)
![seaborn](https://img.shields.io/badge/seaborn-4C72B0?style=for-the-badge&logoColor=white)
![Folium](https://img.shields.io/badge/Folium-77B829?style=for-the-badge&logo=leaflet&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
