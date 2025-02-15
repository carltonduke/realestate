import streamlit as st
import pandas as pd
import numpy as np
import requests
from dotenv import load_dotenv
from os import environ

from scraper.scraper import get_page
from utils.common import get_permits, get_prop_info, get_owner_info

load_dotenv()
URL = environ.get("CORPORATE_URL")

st.set_page_config(
    page_title="property report", page_icon="🖼️", initial_sidebar_state="collapsed"
)

st.session_state["data_store"] = {}

# Start content
st.title('Property Report')
st.text("")

input_container = st.container(border=True)
input_container.header('Address')

text_in_col, go_button_col = input_container.columns([0.8, 0.2])
text = text_in_col.text_input(label="address", label_visibility="collapsed")

if go_button_col.button("Go"):
    if text:
        st.session_state['address'] = text

tab_titles = ["Property", "Owner", "Permits"]
tab1, tab2, tab3 = st.tabs(tab_titles)

if 'address' in st.session_state:
    address = st.session_state['address']
    data_store = st.session_state['data_store']

    if address not in data_store:
        page_source = get_page(URL, address)
        data_store[address] = {'page_source':page_source,
                                'prop_info':None,
                                'owner_info':None,
                                'permits':None}
    
    if not data_store[address]['prop_info']: 
        prop_info = get_prop_info(data_store[address]['page_source'])
        data_store[address]['prop_info'] = prop_info
    else:
        prop_info = data_store[address]['prop_info']

    if not data_store[address]['owner_info']: 
        owner_info = get_owner_info(data_store[address]['page_source'])
        data_store[address]['owner_info'] = owner_info
    else:
        owner_info = data_store[address]['owner_info']

    if not data_store[address]['permits']: 
        df = get_permits(address)
        data_store[address]['permits'] = df
    else:
        df = data_store[address]['permits']

    st.session_state['data_store'] = data_store

    tab1.markdown(f''':blue-background[**ID**]   :blue[{prop_info['Property ID']}]''')
    tab1.markdown(f''':gray-background[**Legal Description**]   :green[{prop_info['Legal Description']}]''')
    tab1.markdown(f''':gray-background[**Property Use**]   :green[{prop_info['Property Use']}]''')
    tab1.markdown(f''':gray-background[**Agent**]   :green[{prop_info['Agent']}]''')

    tab2.markdown(f''':blue-background[**ID**]   :blue[{owner_info['Owner ID']}]''')
    tab2.markdown(f''':gray-background[**Name**]   {owner_info['Name']}''')
    tab2.markdown(f''':gray-background[**State Code**]   {owner_info['State Code']}''')

    tab3.dataframe(df, use_container_width=True)


st.write("")
st.divider()
disclaimer = """We makes no warranties, expressed or implied, concerning the accuracy, completeness, reliability, or suitability of the information provided."""
st.text(disclaimer)
