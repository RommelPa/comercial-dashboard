import streamlit as st

from src.charts import bar, line
from src.data_access import get_margen_cliente, get_ventas_mensuales

st.title("Comercial")

ventas = get_ventas_mensuales()
margen = get_margen_cliente()

if not ventas.empty:
    st.plotly_chart(line(ventas, "periodo", "ingreso_total", "Ventas mensuales"), use_container_width=True)

if not margen.empty:
    top_n = st.slider("Top clientes por margen", min_value=5, max_value=50, value=20, step=5)
    st.plotly_chart(
        bar(margen.head(top_n), "cliente", "margen_total", f"Margen por cliente (Top {top_n})"),
        use_container_width=True,
    )

st.subheader("Tabla de margen por cliente")
st.dataframe(margen, use_container_width=True)
