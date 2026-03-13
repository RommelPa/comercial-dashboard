import streamlit as st

from src.charts import bar
from src.data_access import (
    get_balance_compra_venta,
    get_produccion_por_central,
    get_ventas_mensuales,
)

st.title("Overview")

ventas_df = get_ventas_mensuales()
prod_df = get_produccion_por_central()
balance_df = get_balance_compra_venta()

ventas_totales = float(ventas_df["ingreso_total"].sum()) if not ventas_df.empty else 0.0
energia_vendida = float(ventas_df["energia_vendida_mwh"].sum()) if not ventas_df.empty else 0.0
energia_producida = float(prod_df["energia_mwh"].sum()) if not prod_df.empty else 0.0
balance_total = float(balance_df["balance_compra_venta_mwh"].sum()) if not balance_df.empty else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Ventas totales", f"{ventas_totales:,.0f}")
c2.metric("Energía vendida (MWh)", f"{energia_vendida:,.0f}")
c3.metric("Energía producida (MWh)", f"{energia_producida:,.0f}")
c4.metric("Balance compra vs venta (MWh)", f"{balance_total:,.0f}")

if not ventas_df.empty:
    st.plotly_chart(
        bar(ventas_df, "periodo", "ingreso_total", "Ventas mensuales"),
        use_container_width=True,
    )
if not balance_df.empty:
    st.plotly_chart(
        bar(balance_df, "periodo", "balance_compra_venta_mwh", "Balance compra vs venta (mensual)"),
        use_container_width=True,
    )

st.subheader("Detalle mensual")
st.dataframe(balance_df, use_container_width=True)
