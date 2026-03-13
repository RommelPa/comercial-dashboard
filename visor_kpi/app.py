import streamlit as st

st.set_page_config(page_title="Energy DW Analytics", page_icon="⚡", layout="wide")

st.title("⚡ Energy Data Warehouse Dashboard")
st.markdown(
    """
Dashboard BI profesional conectado al Data Warehouse de energía eléctrica.

**Flujo de datos:** Excel → ETL Python (`etl.load_stg` → `etl.run_dw` → `etl.create_kpis`) → SQL Server (`stg`, `dim`, `fact`, `kpi`) → Streamlit.

La conexión SQL Server se centraliza en `src/database.py` y se configura por `st.secrets["db"]`.

Navega en el menú lateral por:
- Overview
- Comercial
- Operaciones
- Gestión
"""
)
