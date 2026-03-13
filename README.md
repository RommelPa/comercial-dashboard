# ⚡ Comercial Dashboard | BI End-to-End

Proyecto de **Data Engineering + Analytics Engineering + BI** con arquitectura estable:

```text
Excel
  → ETL Python
  → SQL Server Data Warehouse (stg, dim, fact, kpi)
  → Streamlit Dashboard
```

## 1) Arquitectura del proyecto

### Fuentes y ETL
- Fuente principal: Excel.
- Carga y transformación inicial a staging: `etl.load_stg`.
- Construcción del Data Warehouse: `etl.run_dw`.
- Creación de vistas KPI en schema `kpi`: `etl.create_kpis`.

### Data Warehouse
- `stg`: staging tables cargadas desde Excel.
- `dim`: dimensiones (fecha, cliente, mercado, central, tipo de central, división, frecuencia).
- `fact`: hechos (ventas, compras, producción).
- `kpi`: vistas analíticas consumidas por Streamlit.

### Dashboard
- App multipágina en Streamlit:
  - Overview
  - Comercial
  - Operaciones
  - Gestión
- Capa de acceso a datos centralizada en `visor_kpi/src/`.

## 2) Flujo del pipeline

Comando principal (sin cambios):

```bash
python -m etl.pipeline
```

Secuencia interna actual:
1. `etl.load_stg`
2. `etl.run_dw`
3. `etl.create_kpis`

## 3) Configuración de base de datos (segura)

El dashboard lee conexión desde Streamlit secrets:

**Archivo:** `.streamlit/secrets.toml`

```toml
[db]
server = "PC-PRACCOM\\SQLEXPRESS"
database = "DATA_WAREHOUSE"
driver = "ODBC Driver 17 for SQL Server"
```

La conexión usa Windows Authentication (`trusted_connection=yes`) sin usuario/password.

## 4) Estructura del repositorio

```text
visor_kpi/
  app.py
  pages/
    1_Overview.py
    2_Comercial.py
    3_Operaciones.py
    4_Gestion_obligaciones.py
  src/
    database.py
    data_access.py
    filters.py
    queries.py
    charts.py
  sql/
    create_kpis.sql
    views_dashboard.sql
  etl/
    pipeline.py
    load_stg.py
    run_dw.py
    create_kpis.py
```

## 5) Vistas KPI consumidas por la app

- `kpi.vw_energia_vendida_mes`
- `kpi.vw_ingresos_mes`
- `kpi.vw_margen_total`
- `kpi.vw_margen_cliente`
- `kpi.vw_ingresos_mercado`
- `kpi.vw_produccion_total`
- `kpi.vw_produccion_central`
- `kpi.vw_produccion_tipo_central`
- `kpi.vw_balance_energia`
- `kpi.vw_actividades_division`
- `kpi.vw_reportes_frecuencia`
- `kpi.vw_actividades_criticas`
- `kpi.vw_actividades_proximas`

## 6) Ejecutar dashboard

```bash
streamlit run visor_kpi/app.py
```

## 7) Notas de calidad de datos

Las vistas críticas `kpi.vw_margen_total` y `kpi.vw_balance_energia` usan agregación previa por fecha (CTEs) antes del `FULL JOIN`, evitando duplicación por multiplicación de filas entre hechos.
