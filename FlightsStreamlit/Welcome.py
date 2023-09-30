import streamlit as st

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

st.write("# Welcome to Flight Prices Analysis! 👋")

st.sidebar.success("Select a page from the above.")

st.markdown(
    """
    This Streamlit App contains an analysis on business class flight prices in the period ... to ...
"""
)