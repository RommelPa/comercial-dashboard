import streamlit as st

from src.charts import bar, line, pie
from src.data_access import (
    get_balance_energia,
    get_filter_options,
    get_produccion_central,
    get_produccion_tipo_central,
)
from src.filters import render_global_filters

st.title("Operaciones")
st.caption("¿Cuánta energía produjo cada central? ¿Qué tipo de central aporta más? ¿Cuál es el balance compra vs venta?")

filters = render_global_filters(get_filter_options())

prod_central = get_produccion_central(filters)
prod_tipo = get_produccion_tipo_central(filters)
balance = get_balance_energia(filters)

if not prod_central.empty:
    st.plotly_chart(
        bar(prod_central, "NOMBRE_CENTRAL", "produccion", "Producción por central"),
        use_container_width=True,
    )

if not prod_tipo.empty:
    st.plotly_chart(
        pie(prod_tipo, "DESCRIPCION_TIPO_CENTRAL", "produccion", "Producción por tipo de central"),
        use_container_width=True,
    )

if not balance.empty:
    balance_line = balance.copy().reset_index().rename(columns={"index": "periodo"})
    balance_line["periodo"] = balance_line["periodo"] + 1
    st.plotly_chart(line(balance_line, "periodo", "balance", "Balance de energía"), use_container_width=True)
