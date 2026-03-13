import streamlit as st

from src.charts import bar, line, pie
from src.data_access import (
    get_contratos_proximos,
    get_ingresos_mercado,
    get_margen_cliente,
    get_ventas_mensuales,
)

st.title("Comercial")

ventas = get_ventas_mensuales()
margen = get_margen_cliente()
mercado = get_ingresos_mercado()
contratos = get_contratos_proximos()

if not ventas.empty:
    st.plotly_chart(line(ventas, "periodo", "ingreso_total", "Ventas mensuales"), use_container_width=True)
if not margen.empty:
    st.plotly_chart(bar(margen.head(20), "cliente", "margen_total", "Margen por cliente (Top 20)"), use_container_width=True)
if not mercado.empty:
    st.plotly_chart(pie(mercado, "mercado", "ingreso_total", "Ingresos por mercado"), use_container_width=True)

st.subheader("Contratos próximos a vencer")
st.dataframe(contratos, use_container_width=True)
