import streamlit as st
import pandas as pd
import numpy as np



st.title('Llama Lingo')
st.header('Llama Lingo helps you learn a language by chatting with you about object in your surroundings!')


language = st.selectbox(
    'Which language do you want to learn?',
     ['-','Spanish'])

level = st.selectbox(
    'How good are you at speaking '+language+' ?',
     ['Beginner', 'Intermediate', 'Advanced'])

'You selected: ', language, ' at an ', level, ' level.'
st.session_state.language = language

if st.button("Next"):
    st.switch_page("pages/capture.py")