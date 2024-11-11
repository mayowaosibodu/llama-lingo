import json, streamlit as st
import pandas as pd
import numpy as np

st.title('Your Performance Over Time')

with open('performance_history.json', 'r') as f:
	history = json.load(f)


chart_data = pd.DataFrame(history['correct'])

st.line_chart(chart_data)