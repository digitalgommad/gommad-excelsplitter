import io
import math
import os
import zipfile

import pandas as pd
import streamlit as st

# ⚠️ 비밀번호를 바꾸고 싶으면 아래 값만 수정하세요.
SECRET_PASSWORD = "gmexcel2026"

st.set_page_config(
    page_title="디지털곰마드 엑셀 분할기",
    page_icon="🛠️",
    layout="centered",
)

# Streamlit 기본 메뉴, 우측 상단 툴바(Deploy 버튼 포함), 하단 "Made with Streamlit" 배지/푸터를 숨깁니다.
HIDE_STREAMLIT_STYLE = """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        div[data-testid="stToolbar"] {visibility: hidden; height: 0; position: fixed;}
        div[data-testid="stDecoration"] {visibility: hidden; height: 0; position: fixed;}
        div[data-testid="stStatusWidget"] {visibility: hidden; height: 0; position: fixed;}
        div[class^="viewerBadge_container"] {display: none !important;}
        a[class^="viewerBadge_link"] {display: none !important;}
    </style>
"""
st.markdown(HIDE_STREAMLIT_STYLE, unsafe_allow_html=True)

st.title("디지털곰마드 수강생 전용 엑셀 분할기 🛠️")
st.subheader("대용량 엑셀 데이터를 원하는 행 수만큼 깔끔하게 나누어 드립니다.")
st.divider()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False


def check_password() -> None:
    """비밀번호 입력값을 검증하고 세션 상태를 갱신한다."""
    if st.session_state.get("password_input", "") == SECRET_PASSWORD:
        st.session_state.authenticated = True
    else:
        st.session_state.authenticated = False
        st.session_state.password_wrong = True


if not st.session_state.authenticated:
    st.text_input(
        "비밀번호를 입력하세요 🔒",
        type="password",
        key="password_input",
        on_change=check_password,
    )

    if st.session_state.get("password_wrong"):
        st.error("비밀번호가 올바르지 않습니다.")

    st.stop()

# ------------------------------------------------------------------
# 아래는 비밀번호 인증에 성공해야만 보이는 엑셀 분할 기능입니다.
# ------------------------------------------------------------------

st.success("인증되었습니다. 아래에서 엑셀 파일을 분할해 보세요. ✅")

uploaded_file = st.file_uploader(
    "분할할 엑셀 파일을 업로드하세요 (.xlsx, .xls)",
    type=["xlsx", "xls"],
)

col1, col2 = st.columns(2)

with col1:
    header_rows = st.number_input(
        "제목(헤더)으로 사용할 행 수",
        min_value=1,
        max_value=10,
        value=1,
        step=1,
        help="파일 최상단의 제목(헤더) 행 개수입니다. 분할되는 모든 파일 상단에 동일하게 유지됩니다.",
    )

with col2:
    rows_per_file = st.number_input(
        "몇 행씩 나눌까요?",
        min_value=10,
        value=1000,
        step=100,
        help="제목(헤더) 행을 제외한 실제 데이터 행 기준으로 나눕니다.",
    )

# 새 파일이 업로드되면 이전 결과를 초기화합니다.
if uploaded_file is not None and st.session_state.get("last_uploaded_name") != uploaded_file.name:
    st.session_state.pop("zip_data", None)
    st.session_state.pop("zip_file_name", None)
    st.session_state.pop("num_files", None)
    st.session_state["last_uploaded_name"] = uploaded_file.name

if uploaded_file is not None:
    try:
        # 헤더 행을 별도로 다루기 위해 헤더 없이(header=None) 원본 그대로 읽습니다.
        raw_df = pd.read_excel(uploaded_file, header=None)
    except Exception as exc:  # noqa: BLE001
        st.error(f"엑셀 파일을 읽는 중 오류가 발생했습니다: {exc}")
        raw_df = None

    if raw_df is not None:
        header_rows_int = int(header_rows)
        total_rows_all = len(raw_df)

        if total_rows_all <= header_rows_int:
            st.warning("제목(헤더) 행 수가 전체 행 수보다 많거나 같습니다. 제목 행 수를 확인해 주세요.")
        else:
            header_df = raw_df.iloc[:header_rows_int]
            data_df = raw_df.iloc[header_rows_int:].reset_index(drop=True)
            total_data_rows = len(data_df)

            st.caption(
                f"업로드된 파일: **{uploaded_file.name}** · "
                f"제목 **{header_rows_int}행** + 데이터 **{total_data_rows:,}행**, **{len(raw_df.columns)}열**"
            )
            st.dataframe(raw_df.head(header_rows_int + 5), use_container_width=True)

            if st.button("엑셀 분할 시작 🚀", type="primary"):
                if total_data_rows == 0:
                    st.warning("업로드한 엑셀 파일에 데이터가 없습니다.")
                else:
                    try:
                        with st.spinner("엑셀 파일을 분할하고 압축하는 중입니다..."):
                            rows_per_file_int = int(rows_per_file)
                            num_files = math.ceil(total_data_rows / rows_per_file_int)
                            base_name = os.path.splitext(uploaded_file.name)[0]
                            pad = len(str(num_files))

                            zip_buffer = io.BytesIO()
                            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                                for i in range(num_files):
                                    start = i * rows_per_file_int
                                    end = start + rows_per_file_int
                                    chunk_df = data_df.iloc[start:end]

                                    # 제목(헤더) 행을 매 분할 파일 최상단에 동일하게 붙여줍니다.
                                    combined_df = pd.concat([header_df, chunk_df], ignore_index=True)

                                    excel_buffer = io.BytesIO()
                                    with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                                        combined_df.to_excel(writer, index=False, header=False, sheet_name="Sheet1")

                                    file_name = f"{base_name}_{str(i + 1).zfill(pad)}.xlsx"
                                    zip_file.writestr(file_name, excel_buffer.getvalue())

                            zip_buffer.seek(0)

                        st.session_state["zip_data"] = zip_buffer.getvalue()
                        st.session_state["zip_file_name"] = f"{base_name}_분할.zip"
                        st.session_state["num_files"] = num_files
                    except Exception as exc:  # noqa: BLE001
                        st.error(f"엑셀 분할 중 오류가 발생했습니다: {exc}")

if st.session_state.get("zip_data"):
    st.success(f"총 {st.session_state['num_files']}개의 파일로 나누는 작업이 완료되었습니다! 🎉")
    st.download_button(
        label="분할된 엑셀 파일 ZIP 다운로드 📦",
        data=st.session_state["zip_data"],
        file_name=st.session_state["zip_file_name"],
        mime="application/zip",
    )
