"""Conexión reutilizable a SQL Server para el dashboard."""

from __future__ import annotations

import os
from urllib.parse import quote_plus

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def _build_connection_url() -> str:
    """Construye URL SQLAlchemy para SQL Server usando variables de entorno."""
    server = os.getenv("DB_SERVER", "localhost")
    database = os.getenv("DB_NAME", "comercial_dw")
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    trust_cert = os.getenv("DB_TRUST_SERVER_CERTIFICATE", "yes")

    if username and password:
        params = quote_plus(
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};PWD={password};"
            f"TrustServerCertificate={trust_cert};"
        )
    else:
        params = quote_plus(
            f"DRIVER={{{driver}}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"Trusted_Connection=yes;"
            f"TrustServerCertificate={trust_cert};"
        )

    return f"mssql+pyodbc:///?odbc_connect={params}"


@st.cache_resource(show_spinner=False)
def get_engine() -> Engine:
    """Retorna engine cacheado para reutilizar pool de conexiones."""
    return create_engine(_build_connection_url(), pool_pre_ping=True)
