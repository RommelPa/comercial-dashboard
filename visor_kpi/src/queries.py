"""Definición centralizada de queries SQL para el dashboard."""

OVERVIEW_KPIS = """
SELECT
    SUM(ingreso_total) AS ventas_totales,
    SUM(energia_vendida_mwh) AS energia_vendida_mwh,
    SUM(energia_producida_mwh) AS energia_producida_mwh,
    SUM(balance_compra_venta_mwh) AS balance_compra_venta_mwh
FROM kpi.vw_overview_kpis;
"""

VENTAS_MENSUALES = "SELECT * FROM kpi.vw_ventas_mensuales ORDER BY anio, mes;"
MARGEN_CLIENTE = "SELECT * FROM kpi.vw_margen_cliente ORDER BY margen_total DESC;"
INGRESOS_MERCADO = "SELECT * FROM kpi.vw_ingresos_por_mercado ORDER BY ingreso_total DESC;"
CONTRATOS_PROXIMOS = "SELECT * FROM kpi.vw_contratos_proximos_vencer ORDER BY dias_para_vencer;"

PRODUCCION_CENTRAL = "SELECT * FROM kpi.vw_produccion_por_central ORDER BY energia_mwh DESC;"
PRODUCCION_TIPO_CENTRAL = "SELECT * FROM kpi.vw_produccion_por_tipo_central ORDER BY energia_mwh DESC;"
BALANCE_COMPRA_VENTA = "SELECT * FROM kpi.vw_balance_compra_venta ORDER BY anio, mes;"

ACTIVIDADES_DIVISION = "SELECT * FROM kpi.vw_actividades_por_division ORDER BY total_actividades DESC;"
ACTIVIDADES_FRECUENCIA = "SELECT * FROM kpi.vw_actividades_por_frecuencia ORDER BY total_actividades DESC;"
OBLIGACIONES_PROXIMAS = "SELECT * FROM kpi.vw_obligaciones_proximas_vencer ORDER BY fecha_vencimiento;"
ACTIVIDADES_CRITICAS = "SELECT * FROM kpi.vw_actividades_criticas ORDER BY fecha_vencimiento;"
