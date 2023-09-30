import streamlit as st
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression


st.set_page_config(
    page_title="SML",
    page_icon="🛫",
)

df = pd.read_csv("https://raw.githubusercontent.com/imads20/DashApps/main/FlightsStreamlit/cleaned.csv")

X = df[['stop', 'duration_minutes']]
y = df[['price']]

model_ols = LinearRegression()
model_ols.fit(X, y)

def price_predict(stop, duration):
    new_df = pd.DataFrame({
        'stop': [stop], 
        'duration_minutes': [duration]
    })

    prediction = model_ols.predict(new_df)
    prediction_value = prediction[0].round(2)
    string = f"Estimated flight price is ${(prediction_value[0])}"
    
    return string


st.write("# Supervised Machine Learning")

# Horizontal line
st.markdown(
    '<hr style="border: none; height: 5px; background: linear-gradient(90deg, #FFA500, #000000);">',
    unsafe_allow_html=True
)

with st.expander("Click to learn more about the model"):
    st.markdown(
        'This is some text explaning our model'
    )

# Input fields for stop and duration
stop = st.number_input("Number of Stops", min_value=0, max_value=2, step=1, value=0)
duration = st.number_input("Duration (minutes)", min_value=0, value=120, step=30)

# Button to trigger price estimation
if st.button("Estimate Flight Price"):
    result = price_predict(stop, duration)
    st.write(result)