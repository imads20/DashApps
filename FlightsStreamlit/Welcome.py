import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="🛫",
)

st.write("# Welcome to Business Class Flight Prices Analysis! 🛫")

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

st.markdown(
    """
    This Streamlit App contains an analysis on business class flight prices in the period ... to ...

"""
)

st.success("Please select a page from the menu on the left to learn more!")
