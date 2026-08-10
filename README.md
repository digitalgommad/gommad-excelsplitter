# 디지털곰마드 수강생 전용 엑셀 분할기 🛠️

대용량 엑셀 파일을 원하는 행 수만큼 나눠서 ZIP으로 한번에 다운로드할 수 있는 Streamlit 웹 앱입니다.

## 주요 기능

- 비밀번호 인증 (`app.py` 상단의 `SECRET_PASSWORD` 값으로 관리)
- `.xlsx`, `.xls` 파일 업로드
- 원하는 행 수 단위로 엑셀 분할 (헤더 유지)
- 분할된 파일들을 하나의 ZIP으로 압축하여 다운로드

## 설치

```bash
pip install -r requirements.txt
```

## 실행

```bash
streamlit run app.py
```

## 비밀번호 변경

`app.py` 상단의 아래 줄만 수정하면 됩니다.

```python
SECRET_PASSWORD = "GOMMAD2026"
```
