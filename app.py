import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sylva Weekend Itinerary", layout="wide")

st.title("Sylva Weekend Itinerary")
st.write("If you can see this, the Streamlit app is working.")

st.header("Test data load")

try:
    places = pd.read_csv("data/places.csv")
    itinerary = pd.read_csv("data/itinerary.csv")
    packing = pd.read_csv("data/packing.csv")

    st.success("CSV files loaded successfully.")

    st.subheader("Places")
    st.dataframe(places)

    st.subheader("Itinerary")
    st.dataframe(itinerary)

    st.subheader("Packing")
    st.dataframe(packing)

except Exception as e:
    st.error("Something went wrong while loading the data files.")
    st.exception(e)
