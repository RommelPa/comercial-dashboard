"""
tests/test_kpis.py
==================
Validación de cálculos del motor de KPIs.
Usa las interfaces reales de kpi_engine.py y pareto.py.
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config import DATA_PATH


@pytest.fixture(scope="module")
def real_data():
    """Carga los datos del Excel real (skippea si no existe)."""
    if not os.path.exists(DATA_PATH):
        pytest.skip("Archivo no encontrado. Ejecutá: python data/mock/generate_mock_data.py")
    xl = pd.ExcelFile(DATA_PATH)
    ventas = xl.parse("Ventas")
    ventas["fecha"] = pd.to_datetime(ventas["fecha"])
    for col in ["importe_neto", "importe_bruto", "cantidad"]:
        if col in ventas.columns:
            ventas[col] = pd.to_numeric(ventas[col], errors="coerce").fillna(0)
    productos = xl.parse("Productos")
    for col in ["precio_unitario", "costo_unitario"]:
        if col in productos.columns:
            productos[col] = pd.to_numeric(productos[col], errors="coerce")
    return {
        "ventas":     ventas,
        "vendedores": xl.parse("Vendedores"),
        "clientes":   xl.parse("Clientes"),
        "productos":  productos,
        "objetivos":  xl.parse("Objetivos"),
    }


def make_simple_df(n: int = 500, seed: int = 42) -> pd.DataFrame:
    """DataFrame de ventas mínimo para tests unitarios puros."""
    np.random.seed(seed)
    return pd.DataFrame({
        "id_venta":      [f"T{i:04d}" for i in range(n)],
        "fecha":         pd.date_range("2024-01-01", periods=n, freq="6h"),
        "id_vendedor":   np.random.choice(["V001", "V002", "V003"], n),
        "id_cliente":    np.random.choice([f"C{i:03d}" for i in range(30)], n),
        "id_producto":   np.random.choice([f"P{i:02d}" for i in range(20)], n),
        "cantidad":      np.random.randint(1, 50, n),
        "importe_neto":  np.random.uniform(5_000, 200_000, n),
        "importe_bruto": np.random.uniform(6_000, 220_000, n),
        "margen_neto":   np.random.uniform(500, 30_000, n),
        "margen_pct":    np.random.uniform(0.08, 0.35, n),
        "descuento_pct": np.random.uniform(0, 0.12, n),
        "canal":         np.random.choice(["Canal Tradicional", "Supermercadismo", "Mayorista", "HoReCa"], n),
        "zona_vendedor": np.random.choice(["GBA Norte", "GBA Sur", "Interior"], n),
        "nombre_vendedor": np.random.choice(["Juan García", "María López", "Pedro Ruiz"], n),
        "perfil":        np.random.choice(["estrella", "estable", "problematico"], n),
    })


def make_clientes_df(n: int = 30) -> pd.DataFrame:
    np.random.seed(7)
    return pd.DataFrame({
        "id_cliente":   [f"C{i:03d}" for i in range(n)],
        "razon_social": [f"Cliente {i}" for i in range(n)],
        "activo":       True,
        "canal":        np.random.choice(["Canal Tradicional", "Supermercadismo"], n),
        "id_vendedor_asignado": np.random.choice(["V001", "V002", "V003"], n),
    })


def make_objetivos_df() -> pd.DataFrame:
    # Objectives scaled to match test data volume (~$17M per vendor in the period)
    return pd.DataFrame({
        "id_vendedor": ["V001", "V002", "V003"],
        "periodo":     [pd.Timestamp("2024-01-01")] * 3,
        "objetivo":    [20_000_000, 20_000_000, 20_000_000],
    })


# ══════════════════════════════════════════════════════════════
# Tests: calcular_pareto
# ══════════════════════════════════════════════════════════════

def test_pareto_suma_100():
    """La participación_pct del Pareto suma exactamente 1.0 (escala 0-1)."""
    from src.pareto import calcular_pareto
    df = make_simple_df()
    grp = df.groupby("id_producto")["importe_neto"].sum().reset_index()
    result = calcular_pareto(grp, "importe_neto", "id_producto")
    total_pct = result["participacion_pct"].sum()
    assert abs(total_pct - 1.0) < 0.01, f"Suma de participacion_pct: {total_pct:.4f} (esperado ~1.0)"


def test_pareto_categoria_A_cubre_80pct():
    """La categoría A cubre entre 70% y 90% del volumen."""
    from src.pareto import calcular_pareto
    df = make_simple_df()
    grp = df.groupby("id_producto")["importe_neto"].sum().reset_index()
    result = calcular_pareto(grp, "importe_neto", "id_producto")
    total = result["importe_neto"].sum()
    vol_a = result[result["categoria_pareto"] == "A"]["importe_neto"].sum()
    pct_a = vol_a / total
    assert 0.70 <= pct_a <= 0.90, f"Volumen categoría A: {pct_a:.2%} (esperado 70-90%)"


def test_pareto_sin_nulls():
    """Ningún campo del Pareto tiene nulos."""
    from src.pareto import calcular_pareto
    df = make_simple_df()
    grp = df.groupby("id_producto")["importe_neto"].sum().reset_index()
    result = calcular_pareto(grp, "importe_neto", "id_producto")
    for col in ["participacion_pct", "acumulado_pct", "categoria_pareto"]:
        assert result[col].isnull().sum() == 0, f"Nulls en {col}"


def test_pareto_categorias_validas():
    """Las categorías solo son A, B o C."""
    from src.pareto import calcular_pareto
    df = make_simple_df()
    grp = df.groupby("id_producto")["importe_neto"].sum().reset_index()
    result = calcular_pareto(grp, "importe_neto", "id_producto")
    cats_invalidas = set(result["categoria_pareto"].unique()) - {"A", "B", "C"}
    assert not cats_invalidas, f"Categorías inválidas: {cats_invalidas}"


def test_pareto_acumulado_monotono():
    """El acumulado_pct debe ser monotónicamente creciente."""
    from src.pareto import calcular_pareto
    df = make_simple_df()
    grp = df.groupby("id_producto")["importe_neto"].sum().reset_index()
    result = calcular_pareto(grp, "importe_neto", "id_producto")
    diffs = result["acumulado_pct"].diff().dropna()
    assert (diffs >= -0.001).all(), "acumulado_pct no es monotónico creciente"


# ══════════════════════════════════════════════════════════════
# Tests: kpi_ventas_periodo
# ══════════════════════════════════════════════════════════════

def test_kpi_ventas_estructura():
    """kpi_ventas_periodo retorna los campos esperados."""
    from src.kpi_engine import kpi_ventas_periodo
    df = make_simple_df()
    result = kpi_ventas_periodo(df)
    for key in ["importe_total", "transacciones_count", "clientes_unicos"]:
        assert key in result, f"Campo faltante: {key}"


def test_kpi_ventas_positivos():
    """Todos los KPIs de ventas son no negativos."""
    from src.kpi_engine import kpi_ventas_periodo
    df = make_simple_df()
    result = kpi_ventas_periodo(df)
    assert result["importe_total"] > 0
    assert result["transacciones_count"] > 0
    assert result["clientes_unicos"] > 0


def test_kpi_ventas_df_vacio():
    """Con DataFrame vacío retorna ceros."""
    from src.kpi_engine import kpi_ventas_periodo
    df = pd.DataFrame(columns=["importe_neto", "id_venta", "id_cliente"])
    result = kpi_ventas_periodo(df)
    assert result["importe_total"] == 0
    assert result["transacciones_count"] == 0


def test_delta_periodo_conocido():
    """Valida delta cuando período actual = 2× período anterior."""
    from src.kpi_engine import kpi_ventas_periodo
    df_act = pd.DataFrame({
        "id_venta": range(5), "importe_neto": [100_000.0]*5,
        "id_cliente": range(5), "cantidad": [10]*5,
    })
    df_ant = pd.DataFrame({
        "id_venta": range(5), "importe_neto": [50_000.0]*5,
        "id_cliente": range(5), "cantidad": [10]*5,
    })
    res = kpi_ventas_periodo(df_act, df_anterior=df_ant)
    assert res["importe_vs_anterior"] is not None
    assert abs(res["importe_vs_anterior"] - 1.0) < 0.01, (
        f"Delta esperado 100%, obtenido: {res['importe_vs_anterior']:.2%}"
    )


# ══════════════════════════════════════════════════════════════
# Tests: kpi_margen
# ══════════════════════════════════════════════════════════════

def test_kpi_margen_estructura():
    """kpi_margen retorna los campos esperados."""
    from src.kpi_engine import kpi_margen
    df = make_simple_df()
    result = kpi_margen(df)
    for key in ["margen_bruto_total", "margen_pct_promedio"]:
        assert key in result, f"Campo faltante: {key}"


def test_kpi_margen_logico():
    """El margen promedio está en rango 0–100%."""
    from src.kpi_engine import kpi_margen
    df = make_simple_df()
    result = kpi_margen(df)
    assert 0 <= result["margen_pct_promedio"] <= 1.0, (
        f"Margen promedio fuera de rango: {result['margen_pct_promedio']:.2%}"
    )


def test_kpi_margen_sin_columna():
    """Si no hay margen_neto en df, retorna ceros sin error."""
    from src.kpi_engine import kpi_margen
    df = pd.DataFrame({"id_venta": [1], "importe_neto": [10_000]})
    result = kpi_margen(df)
    assert result["margen_bruto_total"] == 0


# ══════════════════════════════════════════════════════════════
# Tests: kpi_cobertura_clientes
# ══════════════════════════════════════════════════════════════

def test_kpi_cobertura_estructura():
    """kpi_cobertura_clientes retorna los campos esperados."""
    from src.kpi_engine import kpi_cobertura_clientes
    df = make_simple_df()
    clientes = make_clientes_df()
    result = kpi_cobertura_clientes(df, clientes)
    for key in ["clientes_activos_periodo", "clientes_total", "cobertura_pct"]:
        assert key in result, f"Campo faltante: {key}"


def test_kpi_cobertura_entre_0_y_1():
    """La cobertura de clientes está entre 0 y 1."""
    from src.kpi_engine import kpi_cobertura_clientes
    df = make_simple_df()
    clientes = make_clientes_df()
    result = kpi_cobertura_clientes(df, clientes)
    assert 0 <= result["cobertura_pct"] <= 1.0, (
        f"Cobertura fuera de [0,1]: {result['cobertura_pct']:.4f}"
    )


def test_kpi_cobertura_total_cuando_todos_compran():
    """Cobertura = 100% cuando todos los clientes activos compraron."""
    from src.kpi_engine import kpi_cobertura_clientes
    ids = ["C001", "C002", "C003"]
    df_v = pd.DataFrame({"id_cliente": ids, "importe_neto": [10_000]*3})
    df_c = pd.DataFrame({"id_cliente": ids, "activo": True})
    result = kpi_cobertura_clientes(df_v, df_c)
    assert result["cobertura_pct"] == 1.0


# ══════════════════════════════════════════════════════════════
# Tests: kpi_por_vendedor
# ══════════════════════════════════════════════════════════════

def test_kpi_por_vendedor_devuelve_dataframe():
    """kpi_por_vendedor retorna DataFrame no vacío."""
    from src.kpi_engine import kpi_por_vendedor
    df  = make_simple_df()
    obj = make_objetivos_df()
    result = kpi_por_vendedor(df, obj)
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0


def test_kpi_por_vendedor_columnas_minimas():
    """El DataFrame contiene las columnas esenciales."""
    from src.kpi_engine import kpi_por_vendedor
    df  = make_simple_df()
    obj = make_objetivos_df()
    result = kpi_por_vendedor(df, obj)
    for col in ["id_vendedor", "importe_total", "transacciones"]:
        assert col in result.columns, f"Columna faltante: {col}"


def test_kpi_cumplimiento_rango():
    """cumplimiento_pct es no negativo (puede superar 1 por sobre-cumplimiento)."""
    from src.kpi_engine import kpi_por_vendedor
    df  = make_simple_df()
    obj = make_objetivos_df()
    result = kpi_por_vendedor(df, obj)
    if "cumplimiento_pct" in result.columns:
        vals = result["cumplimiento_pct"].dropna()
        assert (vals >= 0).all(), "Cumplimientos negativos encontrados"


def test_kpi_ranking_unico_y_consecutivo():
    """Los rankings son únicos y consecutivos desde 1."""
    from src.kpi_engine import kpi_por_vendedor
    df  = make_simple_df()
    obj = make_objetivos_df()
    result = kpi_por_vendedor(df, obj)
    if "ranking_actual" in result.columns:
        rankings = sorted(result["ranking_actual"].tolist())
        assert rankings == list(range(1, len(result) + 1)), "Rankings no son consecutivos"


# ══════════════════════════════════════════════════════════════
# Tests con datos reales (integración)
# ══════════════════════════════════════════════════════════════

def test_total_ventas_real_positivo(real_data):
    from src.kpi_engine import kpi_ventas_periodo
    result = kpi_ventas_periodo(real_data["ventas"])
    assert result["importe_total"] > 0
    print(f"\n  → Total ventas: ${result['importe_total']:,.0f}")
    print(f"  → Transacciones: {result['transacciones_count']:,}")


def test_pareto_con_datos_reales(real_data):
    from src.pareto import calcular_pareto
    ventas = real_data["ventas"]
    grp = ventas.groupby("id_cliente")["importe_neto"].sum().reset_index()
    result = calcular_pareto(grp, "importe_neto", "id_cliente")
    total_pct = result["participacion_pct"].sum()
    assert abs(total_pct - 1.0) < 0.01, f"Suma participacion_pct: {total_pct:.4f} (esperado ~1.0)"
    n_A = (result["categoria_pareto"] == "A").sum()
    print(f"\n  → Clientes cat-A: {n_A}/{len(result)}")


def test_margen_real_razonable(real_data):
    from src.kpi_engine import kpi_margen
    ventas    = real_data["ventas"].copy()
    productos = real_data["productos"].copy()
    # Only merge costo_unitario (ventas already has precio_unitario)
    ventas = ventas.merge(
        productos[["id_producto", "costo_unitario"]],
        on="id_producto", how="left"
    )
    precio = ventas["precio_unitario"].replace(0, np.nan).fillna(1)
    ventas["margen_neto"] = ventas["importe_neto"] * (
        1 - ventas["costo_unitario"].fillna(0) / precio
    )
    result = kpi_margen(ventas)
    assert result["margen_bruto_total"] > 0
    assert 0.01 <= result["margen_pct_promedio"] <= 0.65
    print(f"\n  → Margen promedio real: {result['margen_pct_promedio']:.2%}")
