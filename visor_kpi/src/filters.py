"""Filtros globales de dashboard para todas las páginas."""

from __future__ import annotations

import streamlit as st


def render_global_filters(options: dict) -> dict:
    """Renderiza filtros en sidebar y retorna selección global."""
    with st.sidebar:
        st.header("Filtros globales")

        anio = st.selectbox(
            "Año",
            options=[None] + list(options.get("anios", [])),
            format_func=lambda v: "Todos" if v is None else str(v),
        )

        mes = st.selectbox(
            "Mes",
            options=[None] + list(options.get("meses", [])),
            format_func=lambda v: "Todos" if v is None else str(v).zfill(2),
        )

        cliente = st.multiselect("Cliente", options.get("clientes", []))
        mercado = st.multiselect("Mercado", options.get("mercados", []))
        central = st.multiselect("Central", options.get("centrales", []))
        division = st.multiselect("División", options.get("divisiones", []))

    return {
        "anio": anio,
        "mes": mes,
        "cliente": cliente,
        "mercado": mercado,
        "central": central,
        "division": division,
    }
