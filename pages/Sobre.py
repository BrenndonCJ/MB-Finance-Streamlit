import streamlit as st
import time

with st.spinner('Wait for it...'):
    time.sleep(2)
st.success('Done!')