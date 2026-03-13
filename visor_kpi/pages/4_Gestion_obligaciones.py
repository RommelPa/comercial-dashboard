import streamlit as st

from src.charts import bar, pie
from src.data_access import (
    get_actividades_criticas,
    get_actividades_division,
    get_actividades_proximas,
    get_filter_options,
    get_reportes_frecuencia,
)
from src.filters import render_global_filters

st.title("Gestión")
st.caption(
    "¿Qué actividades tiene cada división? ¿Qué reportes son mensuales, trimestrales o anuales? "
    "¿Qué actividades son críticas? ¿Qué obligaciones están próximas a vencer?"
)

filters = render_global_filters(get_filter_options())

act_div = get_actividades_division(filters)
rep_freq = get_reportes_frecuencia(filters)
act_crit = get_actividades_criticas(filters)
act_prox = get_actividades_proximas(filters)

if not act_div.empty:
    st.plotly_chart(
        bar(act_div, "NOMBRE_DIVISION", "total_actividades", "Actividades por división"),
        use_container_width=True,
    )

if not rep_freq.empty:
    st.plotly_chart(
        pie(rep_freq, "NOMBRE_FRECUENCIA", "total_reportes", "Reportes por frecuencia"),
        use_container_width=True,
    )

st.subheader("Actividades críticas")
st.dataframe(act_crit, use_container_width=True)

st.subheader("Actividades próximas")
st.dataframe(act_prox, use_container_width=True)
