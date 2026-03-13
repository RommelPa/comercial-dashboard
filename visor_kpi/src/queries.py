"""Queries SQL del dashboard (solo vistas KPI disponibles en schema kpi)."""

ENERGIA_VENDIDA_MES = """
SELECT
    ANIO,
    MES,
    energia_vendida_mwh
FROM kpi.vw_energia_vendida_mes
ORDER BY ANIO, MES;
"""

INGRESOS_MES = """
SELECT
    ANIO,
    MES,
    ingresos
FROM kpi.vw_ingresos_mes
ORDER BY ANIO, MES;
"""

MARGEN_TOTAL = """
SELECT
    ingresos,
    costos,
    margen
FROM kpi.vw_margen_total;
"""

MARGEN_CLIENTE = """
SELECT
    NOMBRE_CLIENTE,
    ingresos
FROM kpi.vw_margen_cliente
ORDER BY ingresos DESC;
"""

INGRESOS_MERCADO = """
SELECT
    DESCRIPCION_MERCADO,
    ingresos
FROM kpi.vw_ingresos_mercado
ORDER BY ingresos DESC;
"""

PRODUCCION_TOTAL = """
SELECT
    produccion_total
FROM kpi.vw_produccion_total;
"""

PRODUCCION_CENTRAL = """
SELECT
    NOMBRE_CENTRAL,
    produccion
FROM kpi.vw_produccion_central
ORDER BY produccion DESC;
"""

PRODUCCION_TIPO_CENTRAL = """
SELECT
    DESCRIPCION_TIPO_CENTRAL,
    produccion
FROM kpi.vw_produccion_tipo_central
ORDER BY produccion DESC;
"""

BALANCE_ENERGIA = """
SELECT
    energia_vendida,
    energia_comprada,
    balance
FROM kpi.vw_balance_energia;
"""

ACTIVIDADES_DIVISION = """
SELECT
    NOMBRE_DIVISION,
    total_actividades
FROM kpi.vw_actividades_division
ORDER BY total_actividades DESC;
"""

REPORTES_FRECUENCIA = """
SELECT
    NOMBRE_FRECUENCIA,
    total_reportes
FROM kpi.vw_reportes_frecuencia
ORDER BY total_reportes DESC;
"""

ACTIVIDADES_CRITICAS = """
SELECT
    ACTIVIDAD,
    CRITICIDAD,
    DESTINO
FROM kpi.vw_actividades_criticas;
"""

ACTIVIDADES_PROXIMAS = """
SELECT
    ACTIVIDAD,
    DESTINO,
    DIAS_ALERTA
FROM kpi.vw_actividades_proximas
ORDER BY DIAS_ALERTA ASC;
"""
