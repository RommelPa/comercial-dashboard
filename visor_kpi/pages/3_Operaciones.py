import streamlit as st

from src.charts import bar
from src.data_access import get_balance_compra_venta, get_produccion_por_central

st.title("Operaciones")

prod_central = get_produccion_por_central()
balance = get_balance_compra_venta()

if not prod_central.empty:
    st.plotly_chart(
        bar(prod_central, "central", "energia_mwh", "Producción por central"),
        use_container_width=True,
    )

if not balance.empty:
    st.plotly_chart(
        bar(balance, "periodo", "balance_compra_venta_mwh", "Balance compra vs venta"),
        use_container_width=True,
    )

st.subheader("Detalle de balance")
st.dataframe(balance, use_container_width=True)
