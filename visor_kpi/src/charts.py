"""Componentes reutilizables de visualización con Plotly (tema oscuro)."""

from __future__ import annotations

import pandas as pd
import plotly.express as px

PLOTLY_THEME = "plotly_dark"


def line(df: pd.DataFrame, x: str, y: str, title: str):
    return px.line(df, x=x, y=y, title=title, markers=True, template=PLOTLY_THEME)


def bar(df: pd.DataFrame, x: str, y: str, title: str):
    return px.bar(df, x=x, y=y, title=title, template=PLOTLY_THEME)


def pie(df: pd.DataFrame, names: str, values: str, title: str):
    return px.pie(df, names=names, values=values, title=title, hole=0.35, template=PLOTLY_THEME)
