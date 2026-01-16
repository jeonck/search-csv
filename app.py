import streamlit as st
import pandas as pd

st.set_page_config(page_title="HR 검색", page_icon="🔍", layout="wide")

st.title("HR 사업 검색")

# 파일 업로드와 검색어 입력을 같은 row에 배치
col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])

with col2:
    search_term = st.text_input("🔍 검색어 입력 (성명, 사업명, 주관기관 등)", "")

if uploaded_file is not None:
    # 인코딩 시도
    try:
        df = pd.read_csv(uploaded_file, encoding="cp949")
    except:
        uploaded_file.seek(0)
        try:
            df = pd.read_csv(uploaded_file, encoding="euc-kr")
        except:
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file, encoding="utf-8")

    if search_term:
        # 모든 컬럼에서 검색
        mask = df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)
        filtered_df = df[mask]

        if not filtered_df.empty:
            # 성명, 연월, 사업명, 주관기관, 담당 분야 추출하고 중복 제거
            result_df = filtered_df[["성명", "연월", "사업명", "주관기관", "담당 분야"]].drop_duplicates()

            st.success(f"검색 결과: {len(result_df)}건")
            st.dataframe(result_df, use_container_width=True, hide_index=True)
        else:
            st.warning("검색 결과가 없습니다.")
    else:
        st.info("검색어를 입력하세요.")
else:
    st.info("CSV 파일을 업로드해주세요.")
