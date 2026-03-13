"""Conexión centralizada a SQL Server (Windows Authentication)."""

from __future__ import annotations

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

SERVER = "PC-PRACCOM\\SQLEXPRESS"
DATABASE = "DATA_WAREHOUSE"

CONNECTION_STRING = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server"
    "&trusted_connection=yes"
)


@st.cache_resource(show_spinner=False)
def get_engine() -> Engine:
    """Retorna engine SQLAlchemy cacheado para todo el dashboard."""
    return create_engine(CONNECTION_STRING, pool_pre_ping=True)
