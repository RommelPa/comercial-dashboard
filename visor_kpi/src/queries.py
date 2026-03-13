"""Queries SQL del dashboard (solo vistas KPI disponibles en schema kpi)."""

ENERGIA_VENDIDA_MES = "SELECT * FROM kpi.vw_energia_vendida_mes ORDER BY ANIO, MES;"
INGRESOS_MES = "SELECT * FROM kpi.vw_ingresos_mes ORDER BY ANIO, MES;"
MARGEN_TOTAL = "SELECT * FROM kpi.vw_margen_total;"
MARGEN_CLIENTE = "SELECT * FROM kpi.vw_margen_cliente ORDER BY ingresos DESC;"
INGRESOS_MERCADO = "SELECT * FROM kpi.vw_ingresos_mercado ORDER BY ingresos DESC;"
PRODUCCION_TOTAL = "SELECT * FROM kpi.vw_produccion_total;"
PRODUCCION_CENTRAL = "SELECT * FROM kpi.vw_produccion_central ORDER BY produccion DESC;"
PRODUCCION_TIPO_CENTRAL = (
    "SELECT * FROM kpi.vw_produccion_tipo_central ORDER BY produccion DESC;"
)
BALANCE_ENERGIA = "SELECT * FROM kpi.vw_balance_energia;"
ACTIVIDADES_DIVISION = "SELECT * FROM kpi.vw_actividades_division ORDER BY total_actividades DESC;"
REPORTES_FRECUENCIA = "SELECT * FROM kpi.vw_reportes_frecuencia ORDER BY total_reportes DESC;"
ACTIVIDADES_CRITICAS = "SELECT * FROM kpi.vw_actividades_criticas;"
ACTIVIDADES_PROXIMAS = "SELECT * FROM kpi.vw_actividades_proximas ORDER BY DIAS_ALERTA ASC;"
