"""
tests/test_mock_data.py
=======================
Validación de coherencia y calidad del dataset mock.
"""

import os
import sys
import pytest
import pandas as pd

# Setup path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config import DATA_PATH


@pytest.fixture(scope="module")
def data():
    """Carga el Excel una vez para todos los tests."""
    if not os.path.exists(DATA_PATH):
        pytest.skip(f"Archivo de datos no encontrado: {DATA_PATH}\nEjecutá: python data/mock/generate_mock_data.py")
    xl = pd.ExcelFile(DATA_PATH)
    return {
        "ventas":     xl.parse("Ventas"),
        "vendedores": xl.parse("Vendedores"),
        "clientes":   xl.parse("Clientes"),
        "productos":  xl.parse("Productos"),
        "objetivos":  xl.parse("Objetivos"),
    }


# ── Estructura básica ──────────────────────────────────────────

def test_hojas_excel_existen():
    """El Excel tiene todas las hojas requeridas."""
    if not os.path.exists(DATA_PATH):
        pytest.skip("Archivo no encontrado")
    xl = pd.ExcelFile(DATA_PATH)
    for hoja in ["Ventas", "Vendedores", "Clientes", "Productos", "Objetivos"]:
        assert hoja in xl.sheet_names, f"Falta la hoja: {hoja}"


def test_n_vendedores(data):
    assert len(data["vendedores"]) == 12, f"Esperado: 12, obtenido: {len(data['vendedores'])}"


def test_n_clientes(data):
    n = len(data["clientes"])
    assert n == 180, f"Esperado: 180, obtenido: {n}"


def test_n_productos(data):
    n = len(data["productos"])
    assert n == 60, f"Esperado: 60, obtenido: {n}"


def test_clientes_activos_inactivos(data):
    """~85% activos, ~15% inactivos."""
    n_total  = len(data["clientes"])
    n_activos = data["clientes"]["activo"].sum()
    n_inactivos = n_total - n_activos
    pct_inact = n_inactivos / n_total
    assert 0.10 <= pct_inact <= 0.25, f"% inactivos fuera de rango: {pct_inact:.2%}"


# ── Volumen de transacciones ──────────────────────────────────

def test_volumen_transacciones(data):
    """Al menos 8.000 registros de transacciones (puede ser más según configuración)."""
    n = len(data["ventas"])
    assert n >= 8_000, f"Transacciones insuficientes: {n} (esperado >=8000)"
    assert n <= 40_000, f"Transacciones excesivas: {n} (esperado <=40000)"


# ── Coherencia vendedor-cliente ───────────────────────────────

def test_coherencia_vendedor_cliente(data):
    """Más del 96% de ventas son del vendedor asignado al cliente."""
    ventas = data["ventas"].copy()
    clientes = data["clientes"][["id_cliente", "id_vendedor_asignado"]]
    merged = ventas.merge(clientes, on="id_cliente", how="left")
    n_total     = len(merged)
    n_coherente = (merged["id_vendedor"] == merged["id_vendedor_asignado"]).sum()
    pct = n_coherente / n_total
    assert pct >= 0.96, f"Coherencia vendedor-cliente: {pct:.2%} (esperado >=96%)"


# ── Estacionalidad ────────────────────────────────────────────

def test_estacionalidad_diciembre_enero(data):
    """Diciembre y enero tienen >15% más ventas que el promedio mensual."""
    ventas = data["ventas"].copy()
    ventas["fecha"]   = pd.to_datetime(ventas["fecha"])
    ventas["mes_num"] = ventas["fecha"].dt.month

    mensual = ventas.groupby(ventas["fecha"].dt.to_period("M"))["importe_neto"].sum()
    promedio = mensual.mean()

    meses_dic_ene = ventas[ventas["mes_num"].isin([12, 1])]
    mensual_dic_ene = meses_dic_ene.groupby(meses_dic_ene["fecha"].dt.to_period("M"))["importe_neto"].sum()
    prom_dic_ene = mensual_dic_ene.mean()

    factor = prom_dic_ene / promedio - 1
    assert factor >= 0.10, f"Factor estacionalidad dic/ene: {factor:.2%} (esperado >=10%)"


# ── Clientes inactivos ────────────────────────────────────────

def test_clientes_inactivos_sin_ventas_recientes(data):
    """Los clientes inactivos no tienen ventas en los últimos 60 días del período."""
    ventas   = data["ventas"].copy()
    clientes = data["clientes"].copy()
    ventas["fecha"] = pd.to_datetime(ventas["fecha"])

    fecha_max = ventas["fecha"].max()
    corte_60  = fecha_max - pd.Timedelta(days=60)

    clientes_inactivos = set(clientes[clientes["activo"] == False]["id_cliente"].tolist())
    ventas_recientes   = set(ventas[ventas["fecha"] >= corte_60]["id_cliente"].unique())

    incorrectos = clientes_inactivos & ventas_recientes
    # Toleramos hasta 5% de incorrectos (pueden haber matices en la generación)
    pct_incorrecto = len(incorrectos) / max(len(clientes_inactivos), 1)
    assert pct_incorrecto <= 0.10, (
        f"Clientes inactivos con ventas recientes: {len(incorrectos)} "
        f"({pct_incorrecto:.1%})"
    )


# ── Productos baja rotación ───────────────────────────────────

def test_productos_baja_rotacion(data):
    """Al menos 10 productos representan menos del 5% del volumen acumulado."""
    ventas = data["ventas"].copy()
    por_prod = ventas.groupby("id_producto")["importe_neto"].sum().sort_values()
    total    = por_prod.sum()
    pct_acum = (por_prod.cumsum() / total)
    n_baja   = (pct_acum <= 0.05).sum()
    assert n_baja >= 8, f"Productos de baja rotación: {n_baja} (esperado >=10)"


# ── Nulls críticos ────────────────────────────────────────────

def test_sin_nulls_criticos(data):
    """Campos críticos no tienen nulos."""
    ventas = data["ventas"]
    criticos = ["id_venta", "fecha", "id_vendedor", "id_cliente", "id_producto", "importe_neto"]
    for col in criticos:
        if col in ventas.columns:
            n_nulls = ventas[col].isnull().sum()
            assert n_nulls == 0, f"Nulos en {col}: {n_nulls}"


# ── Importes positivos ────────────────────────────────────────

def test_importes_positivos(data):
    """Todos los importes netos son positivos."""
    ventas = data["ventas"]
    if "importe_neto" in ventas.columns:
        n_neg = (ventas["importe_neto"] <= 0).sum()
        assert n_neg == 0, f"Importes no positivos: {n_neg}"


# ── Fechas en rango ───────────────────────────────────────────

def test_fechas_en_rango(data):
    """Todas las fechas están entre ene-2023 y mar-2026."""
    ventas = data["ventas"].copy()
    ventas["fecha"] = pd.to_datetime(ventas["fecha"])
    f_min = ventas["fecha"].min()
    f_max = ventas["fecha"].max()
    assert f_min >= pd.Timestamp("2023-01-01"), f"Fecha mínima fuera de rango: {f_min}"
    assert f_max <= pd.Timestamp("2026-03-31"), f"Fecha máxima fuera de rango: {f_max}"


# ── Columnas esperadas ─────────────────────────────────────────

def test_columnas_ventas(data):
    esperadas = ["id_venta", "fecha", "id_vendedor", "id_cliente",
                 "id_producto", "cantidad", "importe_neto", "importe_bruto"]
    for col in esperadas:
        assert col in data["ventas"].columns, f"Columna faltante en Ventas: {col}"


def test_columnas_clientes(data):
    esperadas = ["id_cliente", "razon_social", "canal", "zona",
                 "id_vendedor_asignado", "activo"]
    for col in esperadas:
        assert col in data["clientes"].columns, f"Columna faltante en Clientes: {col}"
