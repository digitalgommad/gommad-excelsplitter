# 디지털곰마드 수강생 전용 엑셀 분할기 🛠️

대용량 엑셀 파일을 원하는 행 수만큼 나눠서 ZIP으로 한번에 다운로드할 수 있는 Streamlit 웹 앱입니다.

## 주요 기능

- 비밀번호 인증 (Streamlit Secrets로 관리, 코드에는 비밀번호가 노출되지 않음)
- `.xlsx`, `.xls` 파일 업로드
- 원하는 행 수 단위로 엑셀 분할 (헤더 유지)
- 분할된 파일들을 하나의 ZIP으로 압축하여 다운로드

## 설치

```bash
pip install -r requirements.txt
```

## 비밀번호 설정 (최초 1회)

`.streamlit/secrets.toml.example` 파일을 복사해서 `.streamlit/secrets.toml`로 만들고, 원하는 비밀번호를 입력하세요.
이 파일은 `.gitignore`에 등록되어 있어 GitHub에는 올라가지 않습니다.

```toml
SECRET_PASSWORD = "원하는_비밀번호"
```

## 실행

```bash
streamlit run app.py
```

## Streamlit Community Cloud에 배포할 때 비밀번호 설정

저장소가 공개(Public)이므로, 비밀번호는 반드시 코드가 아닌 **Streamlit Cloud의 Secrets 설정**에 등록해야 합니다.

1. https://share.streamlit.io 에서 배포한 앱 클릭
2. 우측 상단 점 3개(⋮) 메뉴 → **Settings** → **Secrets** 탭
3. 아래 내용 입력 후 저장

```toml
SECRET_PASSWORD = "원하는_비밀번호"
```

4. 저장하면 앱이 자동으로 재시작되며 새 비밀번호가 적용됩니다.

## 비밀번호 변경

로컬에서는 `.streamlit/secrets.toml`, 배포 환경에서는 Streamlit Cloud의 **Secrets** 설정값만 바꾸면 됩니다. (`app.py` 코드는 수정할 필요 없음)
