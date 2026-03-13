import streamlit as st

from src.charts import bar, line
from src.data_access import get_ingresos_mercado, get_ingresos_mes, get_margen_cliente

st.title("Comercial")

ingresos_mes = get_ingresos_mes()
margen_cliente = get_margen_cliente()
ingresos_mercado = get_ingresos_mercado()

if not ingresos_mes.empty:
    ingresos_plot = ingresos_mes.copy()
    ingresos_plot["periodo"] = (
        ingresos_plot["ANIO"].astype(str) + "-" + ingresos_plot["MES"].astype(int).astype(str).str.zfill(2)
    )
    st.plotly_chart(line(ingresos_plot, "periodo", "ingresos", "Ingresos mensuales"), use_container_width=True)

if not margen_cliente.empty:
    top_n = st.slider("Top clientes por ingresos", min_value=5, max_value=50, value=20, step=5)
    st.plotly_chart(
        bar(margen_cliente.head(top_n), "NOMBRE_CLIENTE", "ingresos", f"Ingresos por cliente (Top {top_n})"),
        use_container_width=True,
    )

if not ingresos_mercado.empty:
    st.plotly_chart(
        bar(ingresos_mercado, "DESCRIPCION_MERCADO", "ingresos", "Ingresos por mercado"),
        use_container_width=True,
    )

st.subheader("Tabla de margen por cliente")
st.dataframe(margen_cliente, use_container_width=True)
