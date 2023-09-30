import streamlit as st

st.set_page_config(
    page_title="EDA",
    page_icon="🛫",
)

st.write("# Exploratory Data Analysis")

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

st.sidebar.header('Filters')