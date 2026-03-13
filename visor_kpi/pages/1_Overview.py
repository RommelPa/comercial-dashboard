import pandas as pd
import streamlit as st

from src.charts import bar
from src.data_access import (
    get_balance_energia,
    get_energia_vendida_mes,
    get_ingresos_mes,
    get_margen_total,
    get_produccion_total,
)

st.title("Overview")

energia_df = get_energia_vendida_mes()
ingresos_df = get_ingresos_mes()
produccion_total_df = get_produccion_total()
balance_df = get_balance_energia()
margen_total_df = get_margen_total()

ventas_totales = float(ingresos_df["ingresos"].sum()) if not ingresos_df.empty else 0.0
energia_vendida = float(energia_df["energia_vendida_mwh"].sum()) if not energia_df.empty else 0.0
energia_producida = float(produccion_total_df["produccion_total"].sum()) if not produccion_total_df.empty else 0.0
balance_total = float(balance_df["balance"].sum()) if not balance_df.empty else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Ingresos totales", f"{ventas_totales:,.0f}")
c2.metric("Energía vendida (MWh)", f"{energia_vendida:,.0f}")
c3.metric("Energía producida (MWh)", f"{energia_producida:,.0f}")
c4.metric("Balance energía (MWh)", f"{balance_total:,.0f}")

if not ingresos_df.empty:
    ingresos_plot = ingresos_df.copy()
    ingresos_plot["periodo"] = (
        ingresos_plot["ANIO"].astype(str) + "-" + ingresos_plot["MES"].astype(int).astype(str).str.zfill(2)
    )
    st.plotly_chart(
        bar(ingresos_plot, "periodo", "ingresos", "Ingresos mensuales"),
        use_container_width=True,
    )

if not energia_df.empty:
    energia_plot = energia_df.copy()
    energia_plot["periodo"] = (
        energia_plot["ANIO"].astype(str) + "-" + energia_plot["MES"].astype(int).astype(str).str.zfill(2)
    )
    st.plotly_chart(
        bar(energia_plot, "periodo", "energia_vendida_mwh", "Energía vendida mensual"),
        use_container_width=True,
    )

st.subheader("Balance y margen total")
if not balance_df.empty and not margen_total_df.empty:
    resumen = pd.concat([balance_df.reset_index(drop=True), margen_total_df.reset_index(drop=True)], axis=1)
    st.dataframe(resumen, use_container_width=True)
elif not balance_df.empty:
    st.dataframe(balance_df, use_container_width=True)
elif not margen_total_df.empty:
    st.dataframe(margen_total_df, use_container_width=True)
