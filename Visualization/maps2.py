import plotly.express as px
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'city': ['CDMX', 'GDL', 'MTY'],
    'lat': [19.43, 20.65, 25.68],
    'lon': [-99.13, -103.34, -100.31],
    'value': [10, 20, 15]
})

fig = px.scatter_mapbox(
    df, lat='lat', lon='lon', size='value', hover_name='city',
    color='value', zoom=4, mapbox_style='carto-positron'
)
st.plotly_chart(fig)
