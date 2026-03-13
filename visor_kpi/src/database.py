"""Conexión centralizada a SQL Server usando Streamlit secrets."""

from __future__ import annotations

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def _get_db_config() -> dict:
    if "db" not in st.secrets:
        raise KeyError(
            "Falta la sección [db] en .streamlit/secrets.toml. "
            "Configura server, database y driver."
        )
    return st.secrets["db"]


@st.cache_resource(show_spinner=False)
def get_engine() -> Engine:
    """Retorna engine SQLAlchemy cacheado para todo el dashboard."""
    db = _get_db_config()
    server = db["server"]
    database = db["database"]
    driver = db["driver"].replace(" ", "+")

    connection_string = (
        f"mssql+pyodbc://@{server}/{database}"
        f"?driver={driver}"
        "&trusted_connection=yes"
    )
    return create_engine(connection_string, pool_pre_ping=True)
