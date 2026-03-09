"""
src/pareto.py
=============
Análisis 80/20 para clientes y productos.
"""

import pandas as pd
import numpy as np


def calcular_pareto(
    df: pd.DataFrame,
    columna_valor: str,
    columna_id: str,
) -> pd.DataFrame:
    """
    Agrega columnas de Pareto al DataFrame.

    Returns:
        DataFrame con columnas adicionales:
        - participacion_pct   : % del total (0-1)
        - acumulado_pct       : % acumulado ordenado desc (0-1)
        - categoria_pareto    : 'A' (0-80%), 'B' (80-95%), 'C' (95-100%)
    """
    if df.empty or columna_valor not in df.columns:
        df = df.copy()
        df["participacion_pct"]  = 0.0
        df["acumulado_pct"]      = 0.0
        df["categoria_pareto"]   = "C"
        return df

    df = df.copy()
    total = df[columna_valor].sum()
    if total == 0:
        df["participacion_pct"] = 0.0
        df["acumulado_pct"]     = 0.0
        df["categoria_pareto"]  = "C"
        return df

    # Ordenar descendente por valor
    df = df.sort_values(columna_valor, ascending=False).reset_index(drop=True)
    df["participacion_pct"] = df[columna_valor] / total
    df["acumulado_pct"]     = df["participacion_pct"].cumsum()

    # Categorías
    def _cat(acum: float) -> str:
        if acum <= 0.80:
            return "A"
        elif acum <= 0.95:
            return "B"
        return "C"

    df["categoria_pareto"] = df["acumulado_pct"].apply(_cat)
    return df


def get_concentracion_pareto(
    df: pd.DataFrame,
    columna_valor: str = "importe_total",
) -> dict:
    """
    Métricas de concentración de Pareto.

    Returns:
        dict con:
        - pct_entidades_A  : % de entidades en categoría A
        - pct_ventas_A     : % de ventas que representan
        - n_entidades_A    : cantidad
        - indice_gini      : índice de concentración (0-1)
    """
    if df.empty or "categoria_pareto" not in df.columns:
        return {"pct_entidades_A": 0, "pct_ventas_A": 0,
                "n_entidades_A": 0, "indice_gini": 0}

    total_entidades = len(df)
    total_ventas    = df[columna_valor].sum() if columna_valor in df.columns else 0

    df_A = df[df["categoria_pareto"] == "A"]
    n_A  = len(df_A)
    v_A  = df_A[columna_valor].sum() if columna_valor in df_A.columns else 0

    pct_ent_A   = n_A / total_entidades if total_entidades > 0 else 0
    pct_ventas_A = v_A / total_ventas   if total_ventas > 0 else 0

    # Índice de Gini simplificado
    gini = _calcular_gini(df[columna_valor].values) if columna_valor in df.columns else 0

    return {
        "pct_entidades_A": pct_ent_A,
        "pct_ventas_A":    pct_ventas_A,
        "n_entidades_A":   n_A,
        "indice_gini":     gini,
    }


def _calcular_gini(valores: np.ndarray) -> float:
    """Calcula el índice de Gini (0 = igualdad perfecta, 1 = concentración total)."""
    if len(valores) == 0:
        return 0.0
    valores = np.sort(valores.astype(float))
    n = len(valores)
    idx = np.arange(1, n + 1)
    total = valores.sum()
    if total == 0:
        return 0.0
    return float((2 * (idx * valores).sum() / (n * total)) - (n + 1) / n)
