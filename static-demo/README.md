---
title: Seoul Subway Ridership Dashboard
emoji: 🚇
colorFrom: indigo
colorTo: gray
sdk: static
pinned: false
short_description: 서울 지하철 이용·출퇴근 통근 패턴 인터랙티브 대시보드
---

서울 지하철 이용인원 예측 프로젝트(guro_stream)의 인터랙티브 대시보드입니다.
기존 Streamlit 앱(https://gurostream-process.streamlit.app/)을 대신해,
핵심 인사이트만 큐레이션해 정적 페이지로 재구성했습니다.

- **역별 이용인원 지도** · **출퇴근 순승하차 지도** — folium/Leaflet (직접 클릭·확대)
- **구로디지털단지역 시간대별 순승하차** · **출근 순승하차 상위 역** — 실측 집계 기반 네이티브 차트
- 포트폴리오 상세 페이지에 iframe으로 임베드되며 `postMessage`(`subway-demo-height`)로 높이를 동기화

전처리 코드 덤프 등은 제외하고, 시각적 인사이트(지도 4종 + 차트 2종)만 담았습니다.

## 구성

```
static-demo/
  index.html          대시보드 (Linear 다크 테마, 차트는 inline)
  maps/
    ridership_total.html   역별 이용인원
    ridership_pop.html     이용인원 · 주민등록인구
    diff_morning.html      출근 08–09시 순승하차
    diff_evening.html      퇴근 18–19시 순승하차
```

지도 4개는 원본 `map_visual/`의 folium 산출물을 복사한 것입니다.

## 배포

이 폴더를 HF static space `ingyoun/seoul-subway-demo`에 업로드하면 갱신됩니다.

```python
from huggingface_hub import upload_folder
upload_folder(folder_path=".", repo_id="ingyoun/seoul-subway-demo", repo_type="space")
```

서빙 URL: https://ingyoun-seoul-subway-demo.static.hf.space
