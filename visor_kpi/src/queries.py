"""Queries SQL del dashboard (solo vistas KPI existentes)."""

VENTAS_MENSUALES = "SELECT * FROM kpi.vw_ventas_mensuales ORDER BY anio, mes;"
MARGEN_CLIENTE = "SELECT * FROM kpi.vw_margen_cliente ORDER BY margen_total DESC;"
PRODUCCION_POR_CENTRAL = "SELECT * FROM kpi.vw_produccion_por_central ORDER BY energia_mwh DESC;"
BALANCE_COMPRA_VENTA = "SELECT * FROM kpi.vw_balance_compra_venta ORDER BY anio, mes;"
ACTIVIDADES_POR_DIVISION = "SELECT * FROM kpi.vw_actividades_por_division ORDER BY total_actividades DESC;"
