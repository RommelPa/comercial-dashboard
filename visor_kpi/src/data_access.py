"""Capa de acceso a datos KPI con pandas.read_sql, cache y filtros globales."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd
import streamlit as st

from src import queries
from src.database import get_engine


@st.cache_data(ttl=300, show_spinner=False)
def run_query(sql: str) -> pd.DataFrame:
    """Ejecuta una query contra vistas KPI y retorna un DataFrame."""
    return pd.read_sql(sql, get_engine())


def apply_global_filters(df: pd.DataFrame, filters: dict | None = None) -> pd.DataFrame:
    """Aplica filtros globales de sidebar si las columnas existen en el DataFrame."""
    if filters is None or df.empty:
        return df

    out = df.copy()

    year = filters.get("anio")
    month = filters.get("mes")
    if year and "ANIO" in out.columns:
        out = out[out["ANIO"] == year]
    if month and "MES" in out.columns:
        out = out[out["MES"] == month]

    dim_map = {
        "cliente": "NOMBRE_CLIENTE",
        "mercado": "DESCRIPCION_MERCADO",
        "central": "NOMBRE_CENTRAL",
        "division": "NOMBRE_DIVISION",
    }
    for filter_name, column in dim_map.items():
        selected = filters.get(filter_name)
        if selected and column in out.columns:
            out = out[out[column].isin(selected)]

    return out


def _query_with_filters(sql: str, filters: dict | None = None) -> pd.DataFrame:
    return apply_global_filters(run_query(sql), filters)


def get_energia_vendida_mes(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.ENERGIA_VENDIDA_MES, filters)


def get_ingresos_mes(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.INGRESOS_MES, filters)


def get_margen_total(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.MARGEN_TOTAL, filters)


def get_margen_cliente(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.MARGEN_CLIENTE, filters)


def get_ingresos_mercado(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.INGRESOS_MERCADO, filters)


def get_produccion_total(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.PRODUCCION_TOTAL, filters)


def get_produccion_central(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.PRODUCCION_CENTRAL, filters)


def get_produccion_tipo_central(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.PRODUCCION_TIPO_CENTRAL, filters)


def get_balance_energia(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.BALANCE_ENERGIA, filters)


def get_actividades_division(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.ACTIVIDADES_DIVISION, filters)


def get_reportes_frecuencia(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.REPORTES_FRECUENCIA, filters)


def get_actividades_criticas(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.ACTIVIDADES_CRITICAS, filters)


def get_actividades_proximas(filters: dict | None = None) -> pd.DataFrame:
    return _query_with_filters(queries.ACTIVIDADES_PROXIMAS, filters)


def _unique_values(df: pd.DataFrame, column: str) -> list[str]:
    if column not in df.columns:
        return []
    return sorted(v for v in df[column].dropna().astype(str).unique())


@st.cache_data(ttl=300, show_spinner=False)
def get_filter_options() -> dict[str, Iterable]:
    ingresos = get_ingresos_mes()
    clientes = get_margen_cliente()
    mercados = get_ingresos_mercado()
    centrales = get_produccion_central()
    divisiones = get_actividades_division()

    anios = sorted(int(v) for v in ingresos.get("ANIO", pd.Series(dtype=int)).dropna().unique())
    meses = sorted(int(v) for v in ingresos.get("MES", pd.Series(dtype=int)).dropna().unique())

    return {
        "anios": anios,
        "meses": meses,
        "clientes": _unique_values(clientes, "NOMBRE_CLIENTE"),
        "mercados": _unique_values(mercados, "DESCRIPCION_MERCADO"),
        "centrales": _unique_values(centrales, "NOMBRE_CENTRAL"),
        "divisiones": _unique_values(divisiones, "NOMBRE_DIVISION"),
    }
