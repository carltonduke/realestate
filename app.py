import streamlit as st
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv

from scraper import get_page

load_dotenv()

cache = {}

def get_permits(address):
    """Return table of permits pulled from web api.

    Args:
        address (str): Address to search.

    Returns:
        pandas.DataFrame: Resulting table. Has columns
        ['permittype','permit_type_desc','permit_number', 
        'permit_class', 'permit_location','description','tcad_id', 'total_job_valuation']].
    """
    address = address.upper()
    if address in cache:
        return cache[address]

    URL_BASE = os.environ.get("ADDRESS_URL")
    url = URL_BASE + address

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

    df = pd.DataFrame(data)

    if df.empty:
        print(f"No data found for {address}")
        return None

    df = df[['permittype','permit_type_desc','permit_number', 
             'permit_class', 'permit_location','description',
             'tcad_id', 'total_job_valuation']]

    if address not in cache:
        cache[address] = df

    return df


st.title('Property Verification')

st.subheader('Permit Data')
text = st.text_input("Address")

if st.button("Go"):
    df = get_permits(text)
    st.text("Permits Table")
    st.dataframe(df, use_container_width=True)

    
st.divider()
disclaimer = """We makes no warranties, expressed or implied, concerning the accuracy, completeness, reliability, or suitability of the information provided."""
st.text(disclaimer)
