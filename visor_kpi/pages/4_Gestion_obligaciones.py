import streamlit as st

from src.charts import bar, pie
from src.data_access import (
    get_actividades_criticas,
    get_actividades_division,
    get_actividades_frecuencia,
    get_obligaciones_proximas,
)

st.title("Gestión de obligaciones")

act_div = get_actividades_division()
act_freq = get_actividades_frecuencia()
obl = get_obligaciones_proximas()
crit = get_actividades_criticas()

if not act_div.empty:
    st.plotly_chart(bar(act_div, "division", "total_actividades", "Actividades por división"), use_container_width=True)
if not act_freq.empty:
    st.plotly_chart(pie(act_freq, "frecuencia", "total_actividades", "Actividades por frecuencia"), use_container_width=True)

st.subheader("Obligaciones próximas a vencer")
st.dataframe(obl, use_container_width=True)

st.subheader("Actividades críticas")
st.dataframe(crit, use_container_width=True)
