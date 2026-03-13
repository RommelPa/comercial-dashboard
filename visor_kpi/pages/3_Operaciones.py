import streamlit as st

from src.charts import bar, pie
from src.data_access import get_balance_compra_venta, get_produccion_central, get_produccion_tipo_central

st.title("Operaciones")

prod_central = get_produccion_central()
prod_tipo = get_produccion_tipo_central()
balance = get_balance_compra_venta()

if not prod_central.empty:
    st.plotly_chart(bar(prod_central, "central", "energia_mwh", "Producción por central"), use_container_width=True)
if not prod_tipo.empty:
    st.plotly_chart(pie(prod_tipo, "tipo_central", "energia_mwh", "Producción por tipo de central"), use_container_width=True)

st.subheader("Balance compra vs venta")
st.dataframe(balance, use_container_width=True)
