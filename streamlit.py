

import streamlit as st
import pandas as pd

data = {
    "Year":[2021,2022,2023],
    "Sales":[100,150,200]
}

df = pd.DataFrame(data)

st.line_chart(df.set_index("Year"))
