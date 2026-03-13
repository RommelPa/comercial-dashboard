import streamlit as st

from src.charts import bar
from src.data_access import (
    get_actividades_criticas,
    get_actividades_division,
    get_actividades_proximas,
    get_reportes_frecuencia,
)

st.title("Gestión de obligaciones")

act_div = get_actividades_division()
rep_freq = get_reportes_frecuencia()
act_crit = get_actividades_criticas()
act_prox = get_actividades_proximas()

if not act_div.empty:
    st.plotly_chart(
        bar(act_div, "NOMBRE_DIVISION", "total_actividades", "Actividades por división"),
        use_container_width=True,
    )

if not rep_freq.empty:
    st.plotly_chart(
        bar(rep_freq, "NOMBRE_FRECUENCIA", "total_reportes", "Reportes por frecuencia"),
        use_container_width=True,
    )

st.subheader("Actividades críticas")
st.dataframe(act_crit, use_container_width=True)

st.subheader("Actividades próximas (<= 7 días)")
st.dataframe(act_prox, use_container_width=True)
