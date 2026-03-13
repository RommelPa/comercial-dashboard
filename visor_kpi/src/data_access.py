"""Capa de acceso a datos: ejecuta queries y retorna DataFrames."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.database import get_engine
from src import queries


@st.cache_data(ttl=300, show_spinner=False)
def run_query(sql: str) -> pd.DataFrame:
    return pd.read_sql(sql, get_engine())


def get_overview_kpis() -> pd.DataFrame:
    return run_query(queries.OVERVIEW_KPIS)


def get_ventas_mensuales() -> pd.DataFrame:
    return run_query(queries.VENTAS_MENSUALES)


def get_margen_cliente() -> pd.DataFrame:
    return run_query(queries.MARGEN_CLIENTE)


def get_ingresos_mercado() -> pd.DataFrame:
    return run_query(queries.INGRESOS_MERCADO)


def get_contratos_proximos() -> pd.DataFrame:
    return run_query(queries.CONTRATOS_PROXIMOS)


def get_produccion_central() -> pd.DataFrame:
    return run_query(queries.PRODUCCION_CENTRAL)


def get_produccion_tipo_central() -> pd.DataFrame:
    return run_query(queries.PRODUCCION_TIPO_CENTRAL)


def get_balance_compra_venta() -> pd.DataFrame:
    return run_query(queries.BALANCE_COMPRA_VENTA)


def get_actividades_division() -> pd.DataFrame:
    return run_query(queries.ACTIVIDADES_DIVISION)


def get_actividades_frecuencia() -> pd.DataFrame:
    return run_query(queries.ACTIVIDADES_FRECUENCIA)


def get_obligaciones_proximas() -> pd.DataFrame:
    return run_query(queries.OBLIGACIONES_PROXIMAS)


def get_actividades_criticas() -> pd.DataFrame:
    return run_query(queries.ACTIVIDADES_CRITICAS)
