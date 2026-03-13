import streamlit as st

st.set_page_config(page_title="Energy DW Analytics", page_icon="⚡", layout="wide")

st.title("⚡ Energy Data Warehouse Dashboard")
st.markdown(
    """
Dashboard analítico conectado al Data Warehouse de energía eléctrica.

**Flujo de datos:** Excel → ETL Python → SQL Server (DIM/FACT) → Vistas KPI (`kpi.*`) → Streamlit.

Usa el menú lateral para navegar por:
- Overview
- Comercial
- Operaciones
- Gestión de obligaciones
"""
)

st.info(
    "Configura la conexión con variables de entorno: DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD, DB_DRIVER."
)
