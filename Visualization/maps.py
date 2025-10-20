import pydeck as pdk
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'lat': [19.43, 20.65, 25.68],
    'lon': [-99.13, -103.34, -100.31],
    'value': [100, 70, 85]
})

layer = pdk.Layer(
    'ScatterplotLayer',
    data=df,
    get_position='[lon, lat]',
    get_color='[200, 30, 0, 160]',
    get_radius=50000,
)

view_state = pdk.ViewState(latitude=23, longitude=-102, zoom=4)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
