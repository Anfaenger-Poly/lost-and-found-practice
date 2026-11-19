# 교내 분실물 관리 서비스

교내에서 습득한 물건을 등록하고, 분실물 상태를 관리하는 간단한 웹 서비스입니다.

## 시작하기

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

브라우저에서 `http://127.0.0.1:8000`을 엽니다.

## 현재 기능

- 습득물 등록 (이름, 분류, 습득 장소·날짜, 설명, 보관 장소)
- 최신 등록순 목록과 상태별 필터
- 상세 조회
- 보관 중 / 주인에게 전달됨 상태 변경

데이터는 프로젝트 루트의 SQLite 파일(`lost_and_found.db`)에 저장됩니다.

