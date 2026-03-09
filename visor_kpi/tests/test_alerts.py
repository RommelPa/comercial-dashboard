"""
tests/test_alerts.py
====================
Validación del motor de alertas (ALT001–ALT007).
Usa la interfaz real de alerts_engine.get_alertas_activas().
"""

import os
import sys
import pytest
import pandas as pd
import numpy as np
from datetime import date, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from config import DATA_PATH


# ══════════════════════════════════════════════════════════════
# Fixtures
# ══════════════════════════════════════════════════════════════

def make_ventas_df(hoy=None, seed=42) -> pd.DataFrame:
    """DataFrame de ventas mínimo con ventas en los últimos 90 días."""
    np.random.seed(seed)
    hoy = pd.Timestamp(hoy or date.today())
    rows = []
    for i in range(100):
        f = hoy - pd.Timedelta(days=np.random.randint(0, 90))
        rows.append({
            "id_venta":    f"T{i:04d}",
            "fecha":       f,
            "id_vendedor": np.random.choice(["V001", "V002", "V003"]),
            "id_cliente":  np.random.choice([f"C{j:03d}" for j in range(15)]),
            "id_producto": np.random.choice([f"P{k:02d}" for k in range(10)]),
            "importe_neto": np.random.uniform(10_000, 150_000),
        })
    return pd.DataFrame(rows)


def make_clientes_df(n: int = 15) -> pd.DataFrame:
    return pd.DataFrame({
        "id_cliente":           [f"C{i:03d}" for i in range(n)],
        "razon_social":         [f"Cliente {i}" for i in range(n)],
        "activo":               True,
        "canal":                ["Canal Tradicional"] * n,
        "id_vendedor_asignado": np.random.choice(["V001", "V002", "V003"], n),
    })


def make_productos_df(n: int = 10) -> pd.DataFrame:
    return pd.DataFrame({
        "id_producto": [f"P{i:02d}" for i in range(n)],
        "descripcion": [f"Producto {i}" for i in range(n)],
        "activo":      True,
        "baja_rotacion": False,
    })


def make_objetivos_df(hoy=None) -> pd.DataFrame:
    hoy = pd.Timestamp(hoy or date.today())
    primer_dia = hoy.replace(day=1)
    return pd.DataFrame({
        "id_vendedor": ["V001", "V002", "V003"],
        "periodo":     [primer_dia] * 3,
        "objetivo":    [1_500_000, 1_200_000, 900_000],
    })


def invocar_alertas(df=None, df_ant=None, clientes=None, productos=None, objetivos=None, fecha=None):
    """Helper que llama get_alertas_activas con defaults."""
    from src.alerts_engine import get_alertas_activas
    hoy = date.today()
    return get_alertas_activas(
        df          = df if df is not None else make_ventas_df(),
        df_anterior = df_ant,
        clientes_df = clientes if clientes is not None else make_clientes_df(),
        productos_df= productos if productos is not None else make_productos_df(),
        objetivos_df= objetivos if objetivos is not None else make_objetivos_df(),
        fecha_hasta = fecha or hoy,
    )


# ══════════════════════════════════════════════════════════════
# Schema del DataFrame de alertas
# ══════════════════════════════════════════════════════════════

def test_alertas_retorna_dataframe():
    """get_alertas_activas retorna un DataFrame."""
    result = invocar_alertas()
    assert isinstance(result, pd.DataFrame), "Resultado no es DataFrame"


def test_alertas_esquema_columnas():
    """El DataFrame de alertas tiene todas las columnas requeridas."""
    result = invocar_alertas()
    cols_esperadas = [
        "id_alerta", "nombre", "severidad",
        "entidad_tipo", "entidad_id", "entidad_nombre",
        "valor_actual", "valor_referencia",
        "descripcion_detalle", "fecha_deteccion", "accion_sugerida",
    ]
    for col in cols_esperadas:
        assert col in result.columns, f"Columna faltante en alertas: {col}"


def test_alertas_df_vacio_no_crash():
    """Con DataFrame vacío retorna DataFrame sin errores."""
    from src.alerts_engine import get_alertas_activas
    df_empty = pd.DataFrame(columns=["id_venta", "fecha", "id_vendedor", "id_cliente",
                                      "id_producto", "importe_neto"])
    result = get_alertas_activas(
        df=df_empty,
        df_anterior=None,
        clientes_df=make_clientes_df(),
        productos_df=make_productos_df(),
        objetivos_df=make_objetivos_df(),
    )
    assert isinstance(result, pd.DataFrame)


def test_alertas_severidad_solo_valores_validos():
    """Severidades solo son: alta, media, baja, info."""
    result = invocar_alertas()
    if len(result) > 0:
        invalidas = set(result["severidad"].unique()) - {"alta", "media", "baja", "info"}
        assert not invalidas, f"Severidades inválidas: {invalidas}"


def test_alertas_id_formato_alt():
    """Todos los id_alerta empiezan con 'ALT'."""
    result = invocar_alertas()
    for cod in result["id_alerta"].unique():
        assert cod.startswith("ALT"), f"ID inválido: {cod}"


def test_alertas_no_duplicados_por_entidad():
    """No puede haber dos alertas del mismo tipo para la misma entidad."""
    result = invocar_alertas()
    if len(result) > 1:
        dupes = result.duplicated(subset=["id_alerta", "entidad_id"])
        assert not dupes.any(), f"Alertas duplicadas:\n{result[dupes]}"


# ══════════════════════════════════════════════════════════════
# ALT001: Vendedor con bajo cumplimiento (<65%)
# ══════════════════════════════════════════════════════════════

def test_alt001_se_dispara_con_bajo_cumplimiento():
    """ALT001 aparece cuando un vendedor tiene <65% cumplimiento."""
    from src.alerts_engine import get_alertas_activas
    hoy = pd.Timestamp(date.today())
    primer_dia = hoy.replace(day=1)

    # Objetivo: 1.000.000 — ventas del mes: 200.000 (20% → dispara ALT001)
    df = pd.DataFrame([{
        "id_venta": "T0001",
        "fecha":    hoy - pd.Timedelta(days=2),
        "id_vendedor": "V001",
        "id_cliente":  "C001",
        "id_producto": "P001",
        "importe_neto": 200_000.0,
    }])
    clientes  = make_clientes_df(3)
    productos = make_productos_df(3)
    objetivos = pd.DataFrame([{
        "id_vendedor": "V001",
        "periodo": primer_dia,
        "objetivo": 1_000_000,
    }])

    result = get_alertas_activas(df, None, clientes, productos, objetivos, date.today())
    alt001 = result[result["id_alerta"] == "ALT001"]
    assert len(alt001) >= 1, "ALT001 no se disparó con 20% de cumplimiento"


def test_alt001_no_se_dispara_con_cumplimiento_ok():
    """ALT001 NO aparece cuando un vendedor tiene ≥65% cumplimiento."""
    from src.alerts_engine import get_alertas_activas
    hoy = pd.Timestamp(date.today())
    primer_dia = hoy.replace(day=1)

    # Objetivo: 1.000.000 — ventas del mes: 800.000 (80% → NO dispara)
    df = pd.DataFrame([{
        "id_venta": "T0001",
        "fecha":    hoy - pd.Timedelta(days=2),
        "id_vendedor": "V001",
        "id_cliente":  "C001",
        "id_producto": "P001",
        "importe_neto": 800_000.0,
    }])
    clientes  = make_clientes_df(3)
    productos = make_productos_df(3)
    objetivos = pd.DataFrame([{
        "id_vendedor": "V001",
        "periodo": primer_dia,
        "objetivo": 1_000_000,
    }])

    result = get_alertas_activas(df, None, clientes, productos, objetivos, date.today())
    alt001 = result[result["id_alerta"] == "ALT001"]
    assert len(alt001) == 0, "ALT001 se disparó incorrectamente con 80% cumplimiento"


# ══════════════════════════════════════════════════════════════
# ALT002: Cliente activo sin compras en 45+ días
# ══════════════════════════════════════════════════════════════

def test_alt002_se_dispara_cliente_sin_compra_reciente():
    """ALT002 detecta cliente activo sin compra en 60+ días."""
    from src.alerts_engine import get_alertas_activas
    hoy = pd.Timestamp(date.today())

    # Última compra hace 60 días
    df = pd.DataFrame([{
        "id_venta": "T0001",
        "fecha":    hoy - pd.Timedelta(days=60),
        "id_vendedor": "V001",
        "id_cliente":  "C001",
        "id_producto": "P001",
        "importe_neto": 50_000.0,
    }])
    clientes = pd.DataFrame([{
        "id_cliente": "C001", "razon_social": "Super X",
        "activo": True, "canal": "Canal Tradicional",
        "id_vendedor_asignado": "V001",
    }])
    result = get_alertas_activas(df, None, clientes, make_productos_df(2), None, date.today())
    alt002 = result[result["id_alerta"] == "ALT002"]
    assert len(alt002) >= 1, "ALT002 no detectó cliente sin compra hace 60 días"


def test_alt002_no_se_dispara_con_compra_reciente():
    """ALT002 NO se dispara cuando el cliente compró hace <45 días."""
    from src.alerts_engine import get_alertas_activas
    hoy = pd.Timestamp(date.today())

    df = pd.DataFrame([{
        "id_venta": "T0001",
        "fecha":    hoy - pd.Timedelta(days=5),
        "id_vendedor": "V001",
        "id_cliente":  "C001",
        "id_producto": "P001",
        "importe_neto": 50_000.0,
    }])
    clientes = pd.DataFrame([{
        "id_cliente": "C001", "razon_social": "Super X",
        "activo": True, "canal": "Canal Tradicional",
        "id_vendedor_asignado": "V001",
    }])
    result = get_alertas_activas(df, None, clientes, make_productos_df(2), None, date.today())
    alt002 = result[result["id_alerta"] == "ALT002"]
    assert len(alt002) == 0, "ALT002 se disparó con compra reciente de hace 5 días"


# ══════════════════════════════════════════════════════════════
# ALT004: Producto sin movimiento en 60+ días
# ══════════════════════════════════════════════════════════════

def test_alt004_se_dispara_producto_sin_movimiento():
    """ALT004 detecta producto activo sin ventas en 60+ días."""
    from src.alerts_engine import get_alertas_activas
    hoy = pd.Timestamp(date.today())

    # Última venta del producto hace 70 días
    df = pd.DataFrame([{
        "id_venta": "T0001",
        "fecha":    hoy - pd.Timedelta(days=70),
        "id_vendedor": "V001",
        "id_cliente":  "C001",
        "id_producto": "P001",
        "importe_neto": 10_000.0,
    }])
    productos = pd.DataFrame([{
        "id_producto": "P001", "descripcion": "Aceite 1L",
        "activo": True, "baja_rotacion": False,
    }])
    result = get_alertas_activas(df, None, make_clientes_df(2), productos, None, date.today())
    alt004 = result[result["id_alerta"] == "ALT004"]
    assert len(alt004) >= 1, "ALT004 no detectó producto sin movimiento hace 70 días"


def test_alt004_no_se_dispara_con_venta_reciente():
    """ALT004 NO se dispara cuando el producto vendió recientemente."""
    from src.alerts_engine import get_alertas_activas
    hoy = pd.Timestamp(date.today())

    df = pd.DataFrame([{
        "id_venta": "T0001",
        "fecha":    hoy - pd.Timedelta(days=10),
        "id_vendedor": "V001",
        "id_cliente":  "C001",
        "id_producto": "P001",
        "importe_neto": 10_000.0,
    }])
    productos = pd.DataFrame([{
        "id_producto": "P001", "descripcion": "Aceite 1L",
        "activo": True, "baja_rotacion": False,
    }])
    result = get_alertas_activas(df, None, make_clientes_df(2), productos, None, date.today())
    alt004 = result[result["id_alerta"] == "ALT004"]
    assert len(alt004) == 0, "ALT004 se disparó con venta de hace 10 días"


# ══════════════════════════════════════════════════════════════
# ALT006: Oportunidad (cliente B en crecimiento >30%)
# ══════════════════════════════════════════════════════════════

def test_alt006_no_crashea():
    """ALT006 se evalúa sin lanzar errores."""
    from src.alerts_engine import get_alertas_activas
    hoy = pd.Timestamp(date.today())
    mes_act = hoy.replace(day=1)
    mes_ant = mes_act - pd.DateOffset(months=1)

    ventas_ant = []
    for i in range(3):
        ventas_ant.append({
            "id_venta": f"TA{i}", "id_vendedor": "V001", "id_cliente": "C001",
            "id_producto": "P001",
            "fecha": mes_ant + pd.Timedelta(days=i),
            "importe_neto": 20_000.0,
        })

    ventas_act = []
    for i in range(10):
        ventas_act.append({
            "id_venta": f"TB{i}", "id_vendedor": "V001", "id_cliente": "C001",
            "id_producto": "P001",
            "fecha": mes_act + pd.Timedelta(days=i),
            "importe_neto": 20_000.0,
        })

    df_ant = pd.DataFrame(ventas_ant)
    df_act = pd.DataFrame(ventas_act)
    clientes = pd.DataFrame([{
        "id_cliente": "C001", "razon_social": "Dist. Norte",
        "activo": True, "canal": "Mayorista",
        "id_vendedor_asignado": "V001",
    }])
    result = get_alertas_activas(df_act, df_ant, clientes, make_productos_df(2), None, date.today())
    assert isinstance(result, pd.DataFrame), "ALT006 evaluación lanzó error"


# ══════════════════════════════════════════════════════════════
# Integración con datos reales
# ══════════════════════════════════════════════════════════════

def test_alertas_con_datos_reales():
    """Integración completa con datos del Excel real."""
    if not os.path.exists(DATA_PATH):
        pytest.skip("Archivo de datos no encontrado")

    from src.alerts_engine import get_alertas_activas

    xl = pd.ExcelFile(DATA_PATH)
    ventas    = xl.parse("Ventas")
    clientes  = xl.parse("Clientes")
    productos = xl.parse("Productos")
    objetivos = xl.parse("Objetivos")

    ventas["fecha"]   = pd.to_datetime(ventas["fecha"])
    if "periodo" in objetivos.columns:
        objetivos["periodo"] = pd.to_datetime(objetivos["periodo"])
    else:
        objetivos["periodo"] = pd.to_datetime(
            objetivos[["a\u00f1o", "mes"]].assign(day=1)
        )

    result = get_alertas_activas(
        df=ventas, df_anterior=None,
        clientes_df=clientes, productos_df=productos,
        objetivos_df=objetivos,
    )
    assert isinstance(result, pd.DataFrame)
    print(f"\n  → Alertas detectadas con datos reales: {len(result)}")
    if len(result) > 0:
        for _, row in result.iterrows():
            print(f"    [{row['severidad'].upper():6s}] {row['id_alerta']} — {row['nombre']}")
