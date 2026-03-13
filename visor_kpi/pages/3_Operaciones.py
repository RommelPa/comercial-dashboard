import streamlit as st

from src.charts import bar
from src.data_access import get_balance_energia, get_produccion_central, get_produccion_tipo_central

st.title("Operaciones")

prod_central = get_produccion_central()
prod_tipo = get_produccion_tipo_central()
balance = get_balance_energia()

if not prod_central.empty:
    st.plotly_chart(
        bar(prod_central, "NOMBRE_CENTRAL", "produccion", "Producción por central"),
        use_container_width=True,
    )

if not prod_tipo.empty:
    st.plotly_chart(
        bar(prod_tipo, "DESCRIPCION_TIPO_CENTRAL", "produccion", "Producción por tipo de central"),
        use_container_width=True,
    )

st.subheader("Detalle de balance de energía")
st.dataframe(balance, use_container_width=True)
