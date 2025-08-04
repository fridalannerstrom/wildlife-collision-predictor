import streamlit as st

st.set_page_config(page_title="Wildlife Collision Predictor", layout="centered")

st.title("🚗🦌 Wildlife Collision Predictor")
st.write("Welcome! This app will help predict wildlife-vehicle collision risk based on location and time.")

if st.button("Click here to test!"):
    st.success("Streamlit is working! 🚀")