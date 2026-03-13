import pandas as pd
import streamlit as st

from src.charts import bar, line
from src.data_access import (
    get_balance_energia,
    get_energia_vendida_mes,
    get_filter_options,
    get_ingresos_mes,
    get_margen_total,
    get_produccion_total,
)
from src.filters import render_global_filters

st.title("Overview")

filters = render_global_filters(get_filter_options())

energia_df = get_energia_vendida_mes(filters)
ingresos_df = get_ingresos_mes(filters)
produccion_total_df = get_produccion_total(filters)
balance_df = get_balance_energia(filters)
margen_total_df = get_margen_total(filters)

ventas_totales = float(ingresos_df["ingresos"].sum()) if not ingresos_df.empty else 0.0
energia_vendida = float(energia_df["energia_vendida_mwh"].sum()) if not energia_df.empty else 0.0
energia_producida = float(produccion_total_df["produccion_total"].sum()) if not produccion_total_df.empty else 0.0
balance_total = float(balance_df["balance"].sum()) if not balance_df.empty else 0.0

c1, c2, c3, c4 = st.columns(4)
c1.metric("Ventas totales", f"S/ {ventas_totales:,.0f}")
c2.metric("Energía vendida", f"{energia_vendida:,.0f} MWh")
c3.metric("Energía producida", f"{energia_producida:,.0f} MWh")
c4.metric("Balance energía", f"{balance_total:,.0f} MWh")

if not ingresos_df.empty:
    ingresos_plot = ingresos_df.copy()
    ingresos_plot["periodo"] = (
        ingresos_plot["ANIO"].astype(str) + "-" + ingresos_plot["MES"].astype(int).astype(str).str.zfill(2)
    )
    st.plotly_chart(
        line(ingresos_plot, "periodo", "ingresos", "Ventas mensuales"),
        use_container_width=True,
    )

if not produccion_total_df.empty:
    st.plotly_chart(
        bar(
            pd.DataFrame({"indicador": ["Producción total"], "valor": [energia_producida]}),
            "indicador",
            "valor",
            "Producción total",
        ),
        use_container_width=True,
    )

st.subheader("Balance y margen")
if not balance_df.empty and not margen_total_df.empty:
    resumen = pd.concat([balance_df.reset_index(drop=True), margen_total_df.reset_index(drop=True)], axis=1)
    st.dataframe(resumen, use_container_width=True)
