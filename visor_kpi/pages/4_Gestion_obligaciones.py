import streamlit as st

from src.charts import bar
from src.data_access import get_actividades_por_division

st.title("Gestión de obligaciones")

act_div = get_actividades_por_division()

if not act_div.empty:
    st.plotly_chart(
        bar(act_div, "division", "total_actividades", "Actividades por división"),
        use_container_width=True,
    )

st.subheader("Tabla de actividades por división")
st.dataframe(act_div, use_container_width=True)
