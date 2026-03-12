/* =====================================
   CREAR ESQUEMA KPI
===================================== */

IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'kpi')
BEGIN
    EXEC('CREATE SCHEMA kpi')
END
GO


/* =====================================
   KPIs COMERCIALES
===================================== */

CREATE OR ALTER VIEW kpi.vw_energia_vendida_mes AS
SELECT
    f.ANIO,
    f.MES,
    SUM(v.ENERGIA_MWH) AS energia_vendida_mwh
FROM fact.FACT_VENTA v
JOIN dim.DIM_FECHA f
ON v.ID_FECHA = f.ID_FECHA
GROUP BY
    f.ANIO,
    f.MES
GO


CREATE OR ALTER VIEW kpi.vw_ingresos_mes AS
SELECT
    f.ANIO,
    f.MES,
    SUM(v.IMPORTE_SOLES) AS ingresos
FROM fact.FACT_VENTA v
JOIN dim.DIM_FECHA f
ON v.ID_FECHA = f.ID_FECHA
GROUP BY
    f.ANIO,
    f.MES
GO


CREATE OR ALTER VIEW kpi.vw_margen_total AS
SELECT
    SUM(v.IMPORTE_SOLES) AS ingresos,
    SUM(c.IMPORTE_SOLES) AS costos,
    SUM(v.IMPORTE_SOLES) - SUM(c.IMPORTE_SOLES) AS margen
FROM fact.FACT_VENTA v
LEFT JOIN fact.FACT_COMPRA c
ON v.ID_FECHA = c.ID_FECHA
GO


CREATE OR ALTER VIEW kpi.vw_margen_cliente AS
SELECT
    cl.NOMBRE_CLIENTE,
    SUM(v.IMPORTE_SOLES) AS ingresos
FROM fact.FACT_VENTA v
JOIN dbo.CONTRATO ct
ON v.ID_CONTRATO = ct.ID_CONTRATO
JOIN dim.DIM_CLIENTE cl
ON ct.ID_CLIENTE = cl.ID_CLIENTE
GROUP BY
    cl.NOMBRE_CLIENTE
GO


CREATE OR ALTER VIEW kpi.vw_ingresos_mercado AS
SELECT
    m.DESCRIPCION_MERCADO,
    SUM(v.IMPORTE_SOLES) AS ingresos
FROM fact.FACT_VENTA v
JOIN dbo.CONTRATO ct
ON v.ID_CONTRATO = ct.ID_CONTRATO
JOIN dim.DIM_MERCADO m
ON ct.ID_MERCADO = m.ID_MERCADO
GROUP BY
    m.DESCRIPCION_MERCADO
GO



/* =====================================
   KPIs OPERACIÓN
===================================== */

CREATE OR ALTER VIEW kpi.vw_produccion_total AS
SELECT
    SUM(ENERGIA_MWH) AS produccion_total
FROM fact.FACT_PRODUCCION
GO


CREATE OR ALTER VIEW kpi.vw_produccion_central AS
SELECT
    c.NOMBRE_CENTRAL,
    SUM(p.ENERGIA_MWH) AS produccion
FROM fact.FACT_PRODUCCION p
JOIN dim.DIM_CENTRAL c
ON p.ID_CENTRAL = c.ID_CENTRAL
GROUP BY
    c.NOMBRE_CENTRAL
GO


CREATE OR ALTER VIEW kpi.vw_produccion_tipo_central AS
SELECT
    tc.DESCRIPCION_TIPO_CENTRAL,
    SUM(p.ENERGIA_MWH) AS produccion
FROM fact.FACT_PRODUCCION p
JOIN dim.DIM_CENTRAL c
ON p.ID_CENTRAL = c.ID_CENTRAL
JOIN dim.DIM_TIPO_CENTRAL tc
ON c.ID_TIPO_CENTRAL = tc.ID_TIPO_CENTRAL
GROUP BY
    tc.DESCRIPCION_TIPO_CENTRAL
GO


CREATE OR ALTER VIEW kpi.vw_balance_energia AS
SELECT
    SUM(v.ENERGIA_MWH) AS energia_vendida,
    SUM(c.ENERGIA_MWH) AS energia_comprada,
    SUM(v.ENERGIA_MWH) - SUM(c.ENERGIA_MWH) AS balance
FROM fact.FACT_VENTA v
LEFT JOIN fact.FACT_COMPRA c
ON v.ID_FECHA = c.ID_FECHA
GO



/* =====================================
   KPIs GESTIÓN
===================================== */

CREATE OR ALTER VIEW kpi.vw_actividades_division AS
SELECT
    d.NOMBRE_DIVISION,
    COUNT(*) AS total_actividades
FROM dbo.ACTIVIDAD a
JOIN dim.DIM_DIVISION d
ON a.ID_DIVISION = d.ID_DIVISION
GROUP BY
    d.NOMBRE_DIVISION
GO


CREATE OR ALTER VIEW kpi.vw_reportes_frecuencia AS
SELECT
    f.NOMBRE_FRECUENCIA,
    COUNT(*) AS total_reportes
FROM dbo.ACTIVIDAD a
JOIN dim.DIM_FRECUENCIA f
ON a.ID_FRECUENCIA = f.ID_FRECUENCIA
GROUP BY
    f.NOMBRE_FRECUENCIA
GO


CREATE OR ALTER VIEW kpi.vw_actividades_criticas AS
SELECT
    ACTIVIDAD,
    CRITICIDAD,
    DESTINO
FROM dbo.ACTIVIDAD
WHERE CRITICIDAD = 'Alta'
GO


CREATE OR ALTER VIEW kpi.vw_actividades_proximas AS
SELECT
    ACTIVIDAD,
    DESTINO,
    DIAS_ALERTA
FROM dbo.ACTIVIDAD
WHERE DIAS_ALERTA <= 7
GO