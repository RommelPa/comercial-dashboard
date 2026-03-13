import streamlit as st

from src.charts import bar, line, pie
from src.data_access import (
    get_filter_options,
    get_ingresos_mercado,
    get_ingresos_mes,
    get_margen_cliente,
)
from src.filters import render_global_filters

st.title("Comercial")
st.caption("¿Cuánta energía vendimos por mes? ¿Cuál es el margen por cliente? ¿Qué mercado aporta más ingreso?")

filters = render_global_filters(get_filter_options())

ingresos_mes = get_ingresos_mes(filters)
margen_cliente = get_margen_cliente(filters)
ingresos_mercado = get_ingresos_mercado(filters)

if not ingresos_mes.empty:
    ingresos_plot = ingresos_mes.copy()
    ingresos_plot["periodo"] = (
        ingresos_plot["ANIO"].astype(str) + "-" + ingresos_plot["MES"].astype(int).astype(str).str.zfill(2)
    )
    st.plotly_chart(line(ingresos_plot, "periodo", "ingresos", "Ventas mensuales"), use_container_width=True)

if not margen_cliente.empty:
    st.plotly_chart(
        bar(margen_cliente, "NOMBRE_CLIENTE", "ingresos", "Margen por cliente"),
        use_container_width=True,
    )

if not ingresos_mercado.empty:
    st.plotly_chart(
        pie(ingresos_mercado, "DESCRIPCION_MERCADO", "ingresos", "Ingresos por mercado"),
        use_container_width=True,
    )
