/*
  Vistas KPI usadas por el dashboard.
  Se mantienen solo las vistas requeridas por la app.
*/

CREATE OR ALTER VIEW kpi.vw_ventas_mensuales AS
SELECT
    d.anio,
    d.mes,
    CONCAT(d.anio, '-', RIGHT(CONCAT('0', d.mes), 2)) AS periodo,
    SUM(v.ENERGIA_MWH) AS energia_vendida_mwh,
    SUM(v.MONTO_TOTAL) AS ingreso_total
FROM fact.FACT_VENTA v
JOIN dim.DIM_FECHA d ON d.SK_FECHA = v.SK_FECHA
GROUP BY d.anio, d.mes;
GO

CREATE OR ALTER VIEW kpi.vw_margen_cliente AS
SELECT
    c.NOMBRE_CLIENTE AS cliente,
    SUM(v.MONTO_TOTAL - ISNULL(cp.MONTO_TOTAL, 0)) AS margen_total,
    SUM(v.MONTO_TOTAL) AS ingresos,
    SUM(ISNULL(cp.MONTO_TOTAL, 0)) AS compras_asociadas
FROM fact.FACT_VENTA v
JOIN dim.DIM_CLIENTE c ON c.SK_CLIENTE = v.SK_CLIENTE
LEFT JOIN fact.FACT_COMPRA cp
    ON cp.SK_CLIENTE = v.SK_CLIENTE
   AND cp.SK_FECHA = v.SK_FECHA
GROUP BY c.NOMBRE_CLIENTE;
GO

CREATE OR ALTER VIEW kpi.vw_produccion_por_central AS
SELECT
    ce.NOMBRE_CENTRAL AS central,
    SUM(p.ENERGIA_MWH) AS energia_mwh
FROM fact.FACT_PRODUCCION p
JOIN dim.DIM_CENTRAL ce ON ce.SK_CENTRAL = p.SK_CENTRAL
GROUP BY ce.NOMBRE_CENTRAL;
GO

CREATE OR ALTER VIEW kpi.vw_balance_compra_venta AS
SELECT
    d.anio,
    d.mes,
    CONCAT(d.anio, '-', RIGHT(CONCAT('0', d.mes), 2)) AS periodo,
    SUM(ISNULL(v.ENERGIA_MWH, 0)) - SUM(ISNULL(c.ENERGIA_MWH, 0)) AS balance_compra_venta_mwh,
    SUM(ISNULL(v.ENERGIA_MWH, 0)) AS energia_vendida_mwh,
    SUM(ISNULL(c.ENERGIA_MWH, 0)) AS energia_comprada_mwh
FROM dim.DIM_FECHA d
LEFT JOIN fact.FACT_VENTA v ON v.SK_FECHA = d.SK_FECHA
LEFT JOIN fact.FACT_COMPRA c ON c.SK_FECHA = d.SK_FECHA
GROUP BY d.anio, d.mes;
GO

CREATE OR ALTER VIEW kpi.vw_actividades_por_division AS
SELECT
    d.NOMBRE_DIVISION AS division,
    COUNT(*) AS total_actividades
FROM dbo.ACTIVIDAD a
JOIN dim.DIM_DIVISION d ON d.SK_DIVISION = a.SK_DIVISION
GROUP BY d.NOMBRE_DIVISION;
GO
