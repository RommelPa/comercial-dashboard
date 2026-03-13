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
def get_energia_vendida_mes() -> pd.DataFrame:
    return run_query(queries.ENERGIA_VENDIDA_MES)


@st.cache_data(ttl=300, show_spinner=False)
def get_ingresos_mes() -> pd.DataFrame:
    return run_query(queries.INGRESOS_MES)


@st.cache_data(ttl=300, show_spinner=False)
def get_margen_total() -> pd.DataFrame:
    return run_query(queries.MARGEN_TOTAL)


@st.cache_data(ttl=300, show_spinner=False)
def get_margen_cliente() -> pd.DataFrame:
    return run_query(queries.MARGEN_CLIENTE)


@st.cache_data(ttl=300, show_spinner=False)
def get_ingresos_mercado() -> pd.DataFrame:
    return run_query(queries.INGRESOS_MERCADO)


@st.cache_data(ttl=300, show_spinner=False)
def get_produccion_total() -> pd.DataFrame:
    return run_query(queries.PRODUCCION_TOTAL)


@st.cache_data(ttl=300, show_spinner=False)
def get_produccion_central() -> pd.DataFrame:
    return run_query(queries.PRODUCCION_CENTRAL)


@st.cache_data(ttl=300, show_spinner=False)
def get_produccion_tipo_central() -> pd.DataFrame:
    return run_query(queries.PRODUCCION_TIPO_CENTRAL)


@st.cache_data(ttl=300, show_spinner=False)
def get_balance_energia() -> pd.DataFrame:
    return run_query(queries.BALANCE_ENERGIA)


@st.cache_data(ttl=300, show_spinner=False)
def get_actividades_division() -> pd.DataFrame:
    return run_query(queries.ACTIVIDADES_DIVISION)


@st.cache_data(ttl=300, show_spinner=False)
def get_reportes_frecuencia() -> pd.DataFrame:
    return run_query(queries.REPORTES_FRECUENCIA)


@st.cache_data(ttl=300, show_spinner=False)
def get_actividades_criticas() -> pd.DataFrame:
    return run_query(queries.ACTIVIDADES_CRITICAS)


@st.cache_data(ttl=300, show_spinner=False)
def get_actividades_proximas() -> pd.DataFrame:
    return run_query(queries.ACTIVIDADES_PROXIMAS)
