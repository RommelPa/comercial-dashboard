import streamlit as st

from src.data_access import get_balance_compra_venta, get_overview_kpis
from src.charts import bar

st.title("Overview")

kpi_df = get_overview_kpis()
if kpi_df.empty:
    st.warning("No hay datos en kpi.vw_overview_kpis")
    st.stop()

row = kpi_df.iloc[0]
c1, c2, c3, c4 = st.columns(4)
c1.metric("Ventas totales", f"{row['ventas_totales']:,.0f}")
c2.metric("Energía vendida (MWh)", f"{row['energia_vendida_mwh']:,.0f}")
c3.metric("Energía producida (MWh)", f"{row['energia_producida_mwh']:,.0f}")
c4.metric("Balance compra vs venta (MWh)", f"{row['balance_compra_venta_mwh']:,.0f}")

balance_df = get_balance_compra_venta()
if not balance_df.empty:
    st.plotly_chart(
        bar(balance_df, "periodo", "balance_compra_venta_mwh", "Balance Compra vs Venta"),
        use_container_width=True,
    )

st.dataframe(balance_df, use_container_width=True)
