import streamlit as st
import pandas as pd
import numpy as np
import requests

def get_permits(address):
    address = address.upper()
    url = f"https://data.austintexas.gov/resource/3syk-w9eu.json?original_address1={address}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

    df = pd.DataFrame(data)
    df = df[['permittype','permit_type_desc','permit_number', 
             'permit_class', 'permit_location','description',
             'tcad_id', 'total_job_valuation']]

    return df

st.title('Property Verification')

text = st.text_input("Address")

if st.button("Go"):
    df = get_permits(text)
    st.text("Permits Table")
    st.dataframe(df, use_container_width=True)

