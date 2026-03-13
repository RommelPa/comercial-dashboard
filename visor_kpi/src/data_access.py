"""Capa de acceso a datos KPI con pandas + SQLAlchemy + cache de Streamlit."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src import queries
from src.database import get_engine


@st.cache_data(ttl=300, show_spinner=False)
def run_query(sql: str) -> pd.DataFrame:
    """Ejecuta una query y retorna DataFrame."""
    return pd.read_sql(sql, get_engine())


@st.cache_data(ttl=300, show_spinner=False)
def get_ventas_mensuales() -> pd.DataFrame:
    return run_query(queries.VENTAS_MENSUALES)


@st.cache_data(ttl=300, show_spinner=False)
def get_margen_cliente() -> pd.DataFrame:
    return run_query(queries.MARGEN_CLIENTE)


@st.cache_data(ttl=300, show_spinner=False)
def get_produccion_por_central() -> pd.DataFrame:
    return run_query(queries.PRODUCCION_POR_CENTRAL)


@st.cache_data(ttl=300, show_spinner=False)
def get_balance_compra_venta() -> pd.DataFrame:
    return run_query(queries.BALANCE_COMPRA_VENTA)


@st.cache_data(ttl=300, show_spinner=False)
def get_actividades_por_division() -> pd.DataFrame:
    return run_query(queries.ACTIVIDADES_POR_DIVISION)
