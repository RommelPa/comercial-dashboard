import streamlit as st

st.set_page_config(page_title="Energy DW Analytics", page_icon="⚡", layout="wide")

st.title("⚡ Energy Data Warehouse Dashboard")
st.markdown(
    """
Dashboard analítico conectado al Data Warehouse de energía eléctrica.

**Flujo de datos:** Excel → ETL Python → SQL Server (DIM/FACT) → Vistas KPI (`kpi.*`) → Streamlit.

**Conexión SQL Server (centralizada en `src/database.py`):**
- Server: `PC-PRACCOM\\SQLEXPRESS`
- Database: `DATA_WAREHOUSE`
- Auth: Windows Authentication (`trusted_connection=yes`)
- Driver: `ODBC Driver 17 for SQL Server`

Usa el menú lateral para navegar por:
- Overview
- Comercial
- Operaciones
- Gestión de obligaciones
"""
)
