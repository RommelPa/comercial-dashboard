/* Vistas KPI para dashboard analítico de energía */

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

CREATE OR ALTER VIEW kpi.vw_ingresos_por_mercado AS
SELECT
    m.NOMBRE_MERCADO AS mercado,
    SUM(v.MONTO_TOTAL) AS ingreso_total,
    SUM(v.ENERGIA_MWH) AS energia_mwh
FROM fact.FACT_VENTA v
JOIN dim.DIM_MERCADO m ON m.SK_MERCADO = v.SK_MERCADO
GROUP BY m.NOMBRE_MERCADO;
GO

CREATE OR ALTER VIEW kpi.vw_contratos_proximos_vencer AS
SELECT
    c.ID_CONTRATO AS contrato_id,
    cli.NOMBRE_CLIENTE AS cliente,
    c.FECHA_FIN AS fecha_vencimiento,
    DATEDIFF(DAY, CAST(GETDATE() AS DATE), c.FECHA_FIN) AS dias_para_vencer,
    tc.TIPO_CONTRATO AS tipo_contrato,
    m.NOMBRE_MERCADO AS mercado
FROM dbo.CONTRATO c
JOIN dim.DIM_CLIENTE cli ON cli.SK_CLIENTE = c.SK_CLIENTE
JOIN dim.DIM_TIPO_CONTRATO tc ON tc.SK_TIPO_CONTRATO = c.SK_TIPO_CONTRATO
JOIN dim.DIM_MERCADO m ON m.SK_MERCADO = c.SK_MERCADO
WHERE c.FECHA_FIN >= CAST(GETDATE() AS DATE)
  AND c.FECHA_FIN < DATEADD(DAY, 90, CAST(GETDATE() AS DATE));
GO

CREATE OR ALTER VIEW kpi.vw_produccion_por_central AS
SELECT
    ce.NOMBRE_CENTRAL AS central,
    SUM(p.ENERGIA_MWH) AS energia_mwh
FROM fact.FACT_PRODUCCION p
JOIN dim.DIM_CENTRAL ce ON ce.SK_CENTRAL = p.SK_CENTRAL
GROUP BY ce.NOMBRE_CENTRAL;
GO

CREATE OR ALTER VIEW kpi.vw_produccion_por_tipo_central AS
SELECT
    t.TIPO_CENTRAL AS tipo_central,
    SUM(p.ENERGIA_MWH) AS energia_mwh
FROM fact.FACT_PRODUCCION p
JOIN dim.DIM_CENTRAL c ON c.SK_CENTRAL = p.SK_CENTRAL
JOIN dim.DIM_TIPO_CENTRAL t ON t.SK_TIPO_CENTRAL = c.SK_TIPO_CENTRAL
GROUP BY t.TIPO_CENTRAL;
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

CREATE OR ALTER VIEW kpi.vw_actividades_por_frecuencia AS
SELECT
    f.FRECUENCIA AS frecuencia,
    COUNT(*) AS total_actividades
FROM dbo.ACTIVIDAD a
JOIN dim.DIM_FRECUENCIA f ON f.SK_FRECUENCIA = a.SK_FRECUENCIA
GROUP BY f.FRECUENCIA;
GO

CREATE OR ALTER VIEW kpi.vw_obligaciones_proximas_vencer AS
SELECT
    a.ID_ACTIVIDAD AS actividad_id,
    a.NOMBRE_ACTIVIDAD AS actividad,
    d.NOMBRE_DIVISION AS division,
    f.FRECUENCIA AS frecuencia,
    a.FECHA_VENCIMIENTO AS fecha_vencimiento,
    DATEDIFF(DAY, CAST(GETDATE() AS DATE), a.FECHA_VENCIMIENTO) AS dias_para_vencer,
    a.ESTADO AS estado
FROM dbo.ACTIVIDAD a
JOIN dim.DIM_DIVISION d ON d.SK_DIVISION = a.SK_DIVISION
JOIN dim.DIM_FRECUENCIA f ON f.SK_FRECUENCIA = a.SK_FRECUENCIA
WHERE a.FECHA_VENCIMIENTO >= CAST(GETDATE() AS DATE)
  AND a.FECHA_VENCIMIENTO < DATEADD(DAY, 45, CAST(GETDATE() AS DATE));
GO

CREATE OR ALTER VIEW kpi.vw_actividades_criticas AS
SELECT
    a.ID_ACTIVIDAD AS actividad_id,
    a.NOMBRE_ACTIVIDAD AS actividad,
    d.NOMBRE_DIVISION AS division,
    a.FECHA_VENCIMIENTO AS fecha_vencimiento,
    a.CRITICIDAD AS criticidad,
    a.ESTADO AS estado
FROM dbo.ACTIVIDAD a
JOIN dim.DIM_DIVISION d ON d.SK_DIVISION = a.SK_DIVISION
WHERE a.CRITICIDAD IN ('Alta', 'Crítica');
GO

CREATE OR ALTER VIEW kpi.vw_overview_kpis AS
SELECT
    SUM(v.MONTO_TOTAL) AS ingreso_total,
    SUM(v.ENERGIA_MWH) AS energia_vendida_mwh,
    (SELECT SUM(p.ENERGIA_MWH) FROM fact.FACT_PRODUCCION p) AS energia_producida_mwh,
    SUM(v.ENERGIA_MWH) - (SELECT SUM(c.ENERGIA_MWH) FROM fact.FACT_COMPRA c) AS balance_compra_venta_mwh
FROM fact.FACT_VENTA v;
GO
