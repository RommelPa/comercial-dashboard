# ⚡ excel-to-kpi-dashboard | Energy DW Analytics

Proyecto de portafolio que integra **Data Engineering + Analytics Engineering + BI**:

**Excel → ETL Python → SQL Server DWH → Vistas KPI → Dashboard Streamlit**

## Arquitectura

```text
DATA_WAREHOUSE.xlsx
   ↓
etl/load_stg.py
   ↓
stg.*
   ↓
etl/run_dw.py  (sp_cargar_dw)
   ↓
dim.* + fact.*
   ↓
etl/create_kpis.py + sql/views_dashboard.sql
   ↓
kpi.*
   ↓
Streamlit Dashboard (Overview / Comercial / Operaciones / Gestión)
```

## Pipeline ETL (no modificado)

Ejecución:

```bash
python -m etl.pipeline
```

Flujo:
1. Carga de Excel a staging (`stg.*`).
2. Ejecución de `sp_cargar_dw` para poblar modelo dimensional.
3. Creación/actualización de vistas KPI en schema `kpi`.

## Modelo dimensional

### Dimensiones
- `dim.DIM_CLIENTE`
- `dim.DIM_TIPO_CONTRATO`
- `dim.DIM_MERCADO`
- `dim.DIM_DIVISION`
- `dim.DIM_FRECUENCIA`
- `dim.DIM_FECHA`
- `dim.DIM_TIPO_CENTRAL`
- `dim.DIM_CENTRAL`
- `dim.DIM_CONCEPTO`

### Hechos
- `fact.FACT_VENTA`
- `fact.FACT_COMPRA`
- `fact.FACT_PRODUCCION`
- `fact.FACT_CONSUMO_TIPO_CENTRAL`
- `fact.FACT_MOVIMIENTO_CONCEPTO`
- `fact.FACT_INDICADOR_MENSUAL`

## KPIs del dashboard

### Overview
- Ventas totales
- Energía vendida total
- Energía producida total
- Balance compra vs venta

### Comercial
- Ventas mensuales
- Margen por cliente
- Ingresos por mercado
- Contratos próximos a vencer

### Operaciones
- Producción por central
- Producción por tipo de central
- Balance compra vs venta

### Gestión de obligaciones
- Actividades por división
- Actividades por frecuencia
- Obligaciones próximas a vencer
- Actividades críticas

## Estructura del dashboard

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
    queries.py
    data_access.py
    charts.py
  sql/
    views_dashboard.sql
```

## Configuración

Definir variables de entorno para conexión SQL Server:

- `DB_SERVER`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_DRIVER` (default: `ODBC Driver 17 for SQL Server`)
- `DB_TRUST_SERVER_CERTIFICATE` (default: `yes`)

## Ejecutar dashboard

```bash
streamlit run visor_kpi/app.py
```

## Screenshots (placeholders)

- `![Overview](docs/screenshots/overview.png)`
- `![Comercial](docs/screenshots/comercial.png)`
- `![Operaciones](docs/screenshots/operaciones.png)`
- `![Gestión](docs/screenshots/gestion.png)`
